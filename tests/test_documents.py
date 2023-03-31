import datetime

from httpx import AsyncClient
from sqlalchemy import insert, select

from conftest import client, async_session_maker
from src.models import document


async def test_create_document():
    async with async_session_maker() as session:
        stmt = insert(document).values(
            id=1,
            text='test',
            created_date=datetime.datetime(2019, 1, 20, 14, 9, 2),
            rubrics=["VK-1603736028819866", "VK-75740592382", "VK-34023136930"])
        await session.execute(stmt)
        await session.commit()

        query = select(document)
        result = await session.execute(query)
        assert result.all() == [(
            1,
            'test',
            datetime.datetime(2019, 1, 20, 14, 9, 2),
            ['VK-1603736028819866', 'VK-75740592382', 'VK-34023136930'])]


async def test_document_search(ac: AsyncClient):
    response = await ac.get('/document', params={'text': 'test'})
    assert response.status_code == 200

# async def test_get_specific_operations(ac: AsyncClient):
#     response = await ac.get("/operations", params={
#         "operation_type": "Выплата купонов",
#     })
#
#     assert response.status_code == 200
#     assert response.json()["status"] == "success"
#     assert len(response.json()["data"]) == 1
