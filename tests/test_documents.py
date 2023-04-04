from unittest.mock import patch

from elasticsearch.helpers import bulk

from conftest import client, test_index_name
from models import es_base_client, es


def test_document_search():
    with patch('src.main.es.submit') as mock_es_submit:
        mock_es_submit.return_value = {
            'response': {'hits': {'hits': [{'_source': {'id': 1}}]}}}
        result = client.get('/document/test', headers={'Content-Type': 'application/json'})
        assert result.status_code == 200
        assert len(result.json()) == 1
        assert result.json()[0]['text'] == 'test'


def test_document_not_found():
    with patch('src.main.es.submit') as mock_es_submit:
        mock_es_submit.return_value = {
            'response': {'hits': {'hits': []}}}
        result = client.get('/document/not-exist', headers={'Content-Type': 'application/json'})
        assert result.status_code == 404
        assert result.json() == {'message': 'Not Found'}


def test_elasticsearch_search():
    resp = es_base_client.search(index=test_index_name, q='test')
    assert len(resp['hits']['hits']) == 1
    assert resp['hits']['hits'][0]['_source'] == {'id': 1, 'text': 'test'}
