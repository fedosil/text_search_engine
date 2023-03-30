import pandas as pd
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from src.models import metadata, document, es, index_name

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

metadata.create_all(engine)

df = pd.read_csv('posts.csv')
df['rubrics'] = df['rubrics'].apply(lambda x: [r.strip()[1:-1] for r in x[1:-1].split(',')])
df = df.where(pd.notnull(df), None)

df.to_sql('document', engine, if_exists='append', index=False, method='multi')

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

es.indices.create(index=index_name)

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
