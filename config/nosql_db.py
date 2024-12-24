from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = 'mongodb://localhost:27017'
DATABASE_NAME = 'practice'

client = AsyncIOMotorClient(MONGO_URI)

mongo_db = client[DATABASE_NAME]

def get_database():
    return mongo_db

def get_db():
    try:
        yield mongo_db
    finally:
        pass