from elasticsearch import Elasticsearch
from sqlalchemy import Column, Integer, String, ARRAY, MetaData, Table, TIMESTAMP

from src.config import ES_PASS, ES_PATH_CA_CERTS, ES_USER

metadata = MetaData()

document = Table(
    'document',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True, index=True),
    Column('text', String, nullable=False),
    Column('created_date', TIMESTAMP),
    Column('rubrics', ARRAY(String)),
)

es = Elasticsearch(
    "https://localhost:9200",
    ca_certs=ES_PATH_CA_CERTS,
    basic_auth=(ES_USER, ES_PASS)
)

index_name = 'document'
