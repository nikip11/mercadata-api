import os
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL_MERCADATA"])

database = client.mercadata

