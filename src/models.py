from sqlalchemy import Column, Integer, String, ARRAY, MetaData, Table, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

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


index_name = 'document'
