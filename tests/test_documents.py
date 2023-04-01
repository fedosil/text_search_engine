import datetime
from unittest.mock import patch

from sqlalchemy import insert

from conftest import async_session_maker, client
from src.models import document


async def test_add_document():
    async with async_session_maker() as session:
        stmt = insert(document).values(id=1, text='test', created_date=datetime.datetime(2019, 1, 20, 14, 9, 2),
                                       rubrics=['VK-1603736028819866', 'VK-75740592382', 'VK-34023136930'])
        await session.execute(stmt)
        await session.commit()


async def test_document_search():
    with patch('src.main.es.submit') as mock_es_submit:
        mock_es_submit.return_value = {
            'response': {'hits': {'hits': [{'_source': {'id': 1}}]}}}
        result = client.get('/document/test', headers={'Content-Type': 'application/json'})
        assert result.status_code == 200
        assert len(result.json()) == 1
        assert result.json()[0]['text'] == 'test'


async def test_document_not_found():
    with patch('src.main.es.submit') as mock_es_submit:
        mock_es_submit.return_value = {
            'response': {'hits': {'hits': []}}}
        result = client.get('/document/not-exist', headers={'Content-Type': 'application/json'})
        assert result.status_code == 404
        assert result.json() == {'message': 'Not Found'}


async def test_document_delete():
    with patch('src.main.es_base_client.delete') as mock_es_delete:
        mock_es_delete.return_value = {}
        result = client.delete('/document/1', headers={'Content-Type': 'application/json'})
        assert result.status_code == 200
        assert result.json() == {'message': 'Document deleted', 'document': []}
