from unittest.mock import patch

from conftest import client


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




