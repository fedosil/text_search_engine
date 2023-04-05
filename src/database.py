from typing import AsyncGenerator

from elasticsearch import Elasticsearch
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, ES_HOST, ES_PORT, ES_PATH_CA_CERTS, ES_PASS, ES_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

es_base_client = Elasticsearch(
    f"https://{ES_HOST}:{ES_PORT}",
    ca_certs=ES_PATH_CA_CERTS,
    basic_auth=(ES_USER, ES_PASS)
)

def get_es_base_client():
    yield es_base_client
