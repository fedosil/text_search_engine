import time

from conftest import client, es_base_test_client
from models import index_name


def test_elasticsearch():
    resp = es_base_test_client.search(index=index_name, q='test')
    assert len(resp['hits']['hits']) == 1
    assert resp['hits']['hits'][0]['_source'] == {'id': 1, 'text': 'test'}


def test_document_search():
    result = client.get('/document/test')
    assert result.status_code == 200
    assert len(result.json()) == 1
    assert result.json()[0]['text'] == 'test'


def test_document_delete():
    result = client.delete('/document/1')
    assert result.status_code == 200
    assert result.json()['message'] == 'Document Deleted'
    time.sleep(1)


def test_document_not_found():
    result = client.get('/document/test')
    assert result.status_code == 404
    assert result.json() == {'message': 'Not Found'}


def test_document_delete_not_found():
    result = client.delete('/document/0')
    assert result.status_code == 404
    assert result.json() == {'message': 'Document Not Found'}
