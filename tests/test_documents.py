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


# async def test_document_delete():
#     with patch('src.main.es_base_client.delete') as mock_delete:
#         mock_delete.return_value = {'result': 'deleted', '_id': '1'}
#         result = client.delete('/document/1', headers={'Content-Type': 'application/json'})
#         assert result.status_code == 200
# # async def test_document_delete():
#     with patch('src.main.es_base_client.delete') as mock_es_delete:
#         mock_es_delete.return_value = {'_index': 'document', '_id': '1', '_version': 2, 'result': 'deleted', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 1511, '_primary_term': 2}
#         result = client.delete('/document/1', headers={'Content-Type': 'application/json'})
#         assert result.status_code == 200
#         assert result.json() == {'message': 'Document deleted', 'document': []}
#
#
# async def test_document_delete_not_found():
#     with patch('src.main.es_base_client.delete') as mock_es_delete:
#
#         result = client.delete('/document/1', headers={'Content-Type': 'application/json'})
#         assert result.status_code == 404
#         assert result.json() == {'message': 'Document not found'}
