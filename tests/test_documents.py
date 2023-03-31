import datetime
from unittest.mock import patch

from httpx import AsyncClient
from sqlalchemy import insert

from conftest import async_session_maker
from src.models import document


async def test_document_search(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = insert(document).values(
            id=1,
            text='test',
            created_date=datetime.datetime(2019, 1, 20, 14, 9, 2),
            rubrics=["VK-1603736028819866", "VK-75740592382", "VK-34023136930"])
        await session.execute(stmt)
        await session.commit()
    with patch('src.main.es.submit') as mock_es_submit:
        mock_es_submit.return_value = {
            'response': {'hits': {'hits': [{'_source': {'id': 1}}]}}}
        result = await ac.get('/document/test', headers={'Content-Type': 'application/json'})
        assert result.status_code == 200
        assert len(result.json()) == 1
