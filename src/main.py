import logging
from logging.handlers import RotatingFileHandler

from elasticsearch import NotFoundError, Elasticsearch
from fastapi import FastAPI, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.database import get_async_session, get_es_base_client
from src.models import document, index_name, Document

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add a rotating file handler to the logger
handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 10, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(handler)

app = FastAPI()


@app.get("/document/{text}")
async def document_search(text: str, session: AsyncSession = Depends(get_async_session),
                          es_base_client: Elasticsearch = Depends(get_es_base_client)):
    size = 1000
    search_after = [0]
    id_list = []
    while True:
        try:
            resp = es_base_client.search(index=index_name, q=text, default_operator='AND', df='text', size=size,
                                         sort='id', search_after=search_after)
        except Exception as e:
            logger.error(f"Search Elasticsearch: {str(e)}")
            return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
        if not resp['hits']['hits']:
            break
        search_after = resp['hits']['hits'][-1]['sort']
        id_list.extend(c['_source']['id'] for c in resp['hits']['hits'])
    if id_list:
        query = select(document).filter(document.c.id.in_(id_list)).order_by(document.c.created_date).limit(20)
        try:
            result = await session.execute(query)
        except Exception as e:
            logger.error(f"SQLAlchemy execute: {str(e)}")
            return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
        return result.all()
    return JSONResponse(status_code=404, content={"message": "Not Found"})


@app.delete('/document/{item_id}')
async def document_delete(item_id: int, session: AsyncSession = Depends(get_async_session),
                          es_base_client: Elasticsearch = Depends(get_es_base_client)):
    try:
        es_base_client.delete(index=index_name, id=item_id)
    except NotFoundError:
        logger.warning(f"Document with id {item_id} not found in Elasticsearch")
        return JSONResponse(status_code=404, content={"message": "Document Not Found"})
    query = select(document).filter(document.c.id == item_id)
    try:
        result = await session.execute(query)
    except Exception as e:
        logger.error(f"SQLAlchemy execute: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
    obj = await session.get(Document, item_id)
    await session.delete(obj)
    await session.commit()
    logger.info(f"Document with id {item_id} deleted")
    return {'message': 'Document Deleted', 'document': result.all()}
