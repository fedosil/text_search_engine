from elasticsearch import Elasticsearch
from elasticsearch.client import AsyncSearchClient
from sqlalchemy import Column, Integer, String, ARRAY, MetaData, Table, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

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

Base = declarative_base()


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, nullable=False)
    created_date = Column(TIMESTAMP)
    rubrics = Column(ARRAY(String))


es_base_client = Elasticsearch(
    "https://localhost:9200",
    ca_certs=ES_PATH_CA_CERTS,
    basic_auth=(ES_USER, ES_PASS)
)

es = AsyncSearchClient(es_base_client)

index_name = 'document'
