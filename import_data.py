import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine, Column, Integer, String, ARRAY, MetaData, Table, TIMESTAMP

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, ES_PASS, ES_PATH_CA_CERTS, ES_USER

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
metadata = MetaData()

document = Table(
    'document',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True, index=True),
    Column('text', String, nullable=False),
    Column('created_date', TIMESTAMP),
    Column('rubrics', ARRAY(String)),
)

metadata.create_all(engine)

df = pd.read_csv('posts.csv')
df['rubrics'] = df['rubrics'].apply(lambda x: [r.strip()[1:-1] for r in x[1:-1].split(',')])
df = df.where(pd.notnull(df), None)

df.to_sql('document', engine, if_exists='append', index=False, method='multi')

es = Elasticsearch(
    "https://localhost:9200",
    ca_certs=ES_PATH_CA_CERTS,
    basic_auth=(ES_USER, ES_PASS)
)

# print(es.info)
index_name = 'my_index'
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

body = {
    'mappings': {
        'properties': {
            'id': {'type': 'integer'},
            'text': {'type': 'text'}
        }
    }
}

es.indices.create(index='my_index')

# index data in Elasticsearch
conn = engine.connect()
stmt = document.select()
result = conn.execute(stmt)

bulk_data = []

for row in result:
    bulk_data.append({
        '_index': index_name,
        '_id': row['id'],
        'id': row['id'],
        'text': row['text']
    })

bulk(es, bulk_data)
