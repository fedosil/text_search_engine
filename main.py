from fastapi import FastAPI, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.database import engine
from src.models import document, es, index_name, es_base_client, Document

app = FastAPI()


@app.get("/search/{text}")
async def document_search(text: str, session: AsyncSession = Depends(get_async_session)):
    resp = es.submit(index=index_name, q=text)
    id_list = [c['_source']['id'] for c in resp['response']['hits']['hits']]
    query = select(document).filter(document.c.id.in_(id_list)).order_by(document.c.created_date).limit(20)
    result = await session.execute(query)
    # result = [{'id': pk, 'text': text, 'created_date': created_date, 'rubrics': rubrics}
    #           for pk, text, created_date, rubrics in execute.fetchall()]
    return result.all()


@app.delete('/document/{_id}')
async def document_delete(_id: int, session: AsyncSession = Depends(get_async_session)):
    es_base_client.delete(index=index_name, id=_id)
    obj = await session.get(Document, _id)
    await session.delete(obj)
    await session.commit()
    return {'message': 'Document deleted'}

# @app.get('/document/{_id}')
# async def document_delete(_id: int):
#     async with engine.connect() as conn:
#         execute = await conn.execute(select(document).where(document.c.id == _id))
#         response = [{'id': pk, 'text': text, 'created_date': created_date, 'rubrics': rubrics}
#                     for pk, text, created_date, rubrics in execute.fetchall()]
#         return response
