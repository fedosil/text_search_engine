import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ARRAY, MetaData, Table, TIMESTAMP

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

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
