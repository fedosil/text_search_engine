from elasticsearch import NotFoundError
from fastapi import FastAPI, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.database import get_async_session
from src.models import document, es, index_name, es_base_client, Document

app = FastAPI()



@app.get("/document/{text}")
async def document_search(text: str, session: AsyncSession = Depends(get_async_session)):
    resp = es.submit(index=index_name, q=text, default_operator='AND', df='text', size=10000)
    id_list = [c['_source']['id'] for c in resp['response']['hits']['hits']]
    print(len(id_list))
    if id_list:
        query = select(document).filter(document.c.id.in_(id_list)).order_by(document.c.created_date).limit(20)
        result = await session.execute(query)
        return result.all()
    return JSONResponse(status_code=404, content={"message": "Not Found"})


@app.delete('/document/{id}')
async def document_delete(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        es_base_client.delete(index=index_name, id=item_id)
        query = select(document).filter(document.c.id == item_id)
        result = await session.execute(query)
        obj = await session.get(Document, item_id)
        await session.delete(obj)
        await session.commit()
        return {'message': 'Document deleted', 'document': result.all()}
    except NotFoundError:
        return JSONResponse(status_code=404, content={"message": "Document not found"})
