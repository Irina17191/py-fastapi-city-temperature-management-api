from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city_crud_api import models, schemas


async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.City).offset(skip).limit(limit))
    cities = result.scalars().all()
    return cities


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.City).filter(models.City.id == city_id))
    city = result.scalar_one_or_none()
    return city


async def update_city(db: AsyncSession, city_id: int, city_update: schemas.CityCreate):
    result = await db.execute(select(models.City).filter(models.City.id == city_id))
    db_city = result.scalars().first()
    if db_city is None:
        return None
    db_city.name = city_update.name
    db_city.additional_info = city_update.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.City).filter(models.City.id == city_id))
    db_city = result.scalars().first()
    if db_city:
        await db.delete(db_city)
        await db.commit()
        return db_city
    return None
