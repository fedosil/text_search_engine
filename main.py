from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import document, es, index_name

app = FastAPI()


@app.get("/search/{text}")
async def document_search(text: str, session: AsyncSession = Depends(get_async_session)):
    resp = es.search(index=index_name, q=text)
    id_list = [c['_source']['id'] for c in resp['hits']['hits']]
    query = select(document).filter(document.c.id.in_(id_list)).limit(20)
    result = await session.execute(query)
    return result.all()


@app.get("/")
async def get_specific_operations(session: AsyncSession = Depends(get_async_session)):
    query = select(document).limit(20)
    result = await session.execute(query)
    return result.all()
