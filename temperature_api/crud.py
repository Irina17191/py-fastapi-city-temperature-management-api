from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city_crud_api import models, schemas


async def create_temperature(db: AsyncSession, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(**temperature.dict())
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def get_temperatures(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Temperature).offset(skip).limit(limit))
    return result.scalars().all()


async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.Temperature).filter(models.Temperature.city_id == city_id))
    return result.scalars().all()
