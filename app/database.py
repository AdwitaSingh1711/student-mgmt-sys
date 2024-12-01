from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("student_management")
collection = db["students"]
