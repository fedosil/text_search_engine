from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_async_session
from .models import document

app = FastAPI()


@app.get("/search/{text}")
async def document_search(text: str):
    return {"message": text}


@app.get("/")
async def get_specific_operations(session: AsyncSession = Depends(get_async_session)):
    query = select(document)
    execute = await session.execute(query)
    result = [{'id': _id, 'rubrics': rubrics, 'text': text, 'date': date} for _id, rubrics, text, date in execute.all()]
    return result
