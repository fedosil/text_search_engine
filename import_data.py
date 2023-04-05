import pandas as pd
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine

from src.database import es_base_client
from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from src.models import metadata, document, index_name

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

metadata.create_all(engine)

df = pd.read_csv('posts.csv')
df['rubrics'] = df['rubrics'].apply(lambda x: [r.strip()[1:-1] for r in x[1:-1].split(',')])
df = df.where(pd.notnull(df), None)

df.to_sql('document', engine, if_exists='append', index=False, method='multi')

if es_base_client.indices.exists(index=index_name):
    es_base_client.indices.delete(index=index_name)

es_base_client.indices.create(index=index_name)

conn = engine.connect()
stmt = document.select()
result = conn.execute(stmt)

bulk_data = []

for row in result.fetchall():
    bulk_data.append({
        '_index': index_name,
        '_id': row[0],
        'id': row[0],
        'text': row[1]
    })

bulk(es_base_client, bulk_data)
