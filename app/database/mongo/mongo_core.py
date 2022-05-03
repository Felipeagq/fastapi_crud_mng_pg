import motor.motor_asyncio

from app.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_DATABASE_URL
)

mg_database = client["books"]