from elasticsearch import NotFoundError, Elasticsearch
from fastapi import FastAPI, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.database import get_async_session, get_es_base_client
from src.models import document, index_name, Document

app = FastAPI()


@app.get("/document/{text}")
async def document_search(text: str, session: AsyncSession = Depends(get_async_session),
                          es_base_client: Elasticsearch = Depends(get_es_base_client)):
    resp = es_base_client.search(index=index_name, q=text, default_operator='AND', df='text', size=10000)
    id_list = [c['_source']['id'] for c in resp['hits']['hits']]
    if id_list:
        query = select(document).filter(document.c.id.in_(id_list)).order_by(document.c.created_date).limit(20)
        result = await session.execute(query)
        return result.all()
    return JSONResponse(status_code=404, content={"message": "Not Found"})


@app.delete('/document/{item_id}')
async def document_delete(item_id: int, session: AsyncSession = Depends(get_async_session),
                          es_base_client: Elasticsearch = Depends(get_es_base_client)):
    try:
        es_base_client.delete(index=index_name, id=item_id)
    except NotFoundError:
        return JSONResponse(status_code=404, content={"message": "Document not found"})
    query = select(document).filter(document.c.id == item_id)
    result = await session.execute(query)
    obj = await session.get(Document, item_id)
    await session.delete(obj)
    await session.commit()
    return {'message': 'Document deleted', 'document': result.all()}
