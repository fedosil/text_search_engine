import datetime

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, ARRAY

metadata = MetaData()

document = Table(
    'document',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True, index=True),
    Column('rubrics', ARRAY(String)),
    Column('text', String, nullable=False),
    Column('created_at', TIMESTAMP),
)
