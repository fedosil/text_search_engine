import pytest

from fastapi.testclient import TestClient
from src.database import get_async_session
from src.main import app
from unittest.mock import patch

client = TestClient(app)


@pytest.fixture(scope='module')
def session():
    async_session = get_async_session()
    yield async_session
    async_session.aclose()


@pytest.mark.asyncio
async def test_document_search(session):
    with patch('src.main.es.submit') as mock_es_submit:
        mock_es_submit.return_value = {
            'response': {'hits': {'hits': [{'_source': {'id': 99}}, {'_source': {'id': 98}}]}}}
        result = client.get('/document/test', headers={'Content-Type': 'application/json'})
        assert result.status_code == 200
        assert len(result.json()) == 2


@pytest.mark.asyncio
async def test_document_search_not_found(session):
    with patch('src.main.es.submit') as mock_es_submit:
        mock_es_submit.return_value = {'response': {'hits': {'hits': []}}}
        result = client.get('/document/non-existing', headers={'Content-Type': 'application/json'})
        assert result.status_code == 404
        assert result.json() == {'message': 'Not Found'}
