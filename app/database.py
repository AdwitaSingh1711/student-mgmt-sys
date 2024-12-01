from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
# MONGO_URI="mongodb+srv://adwitasat07:Gpt32w0cTqLKC9F8@cluster0.iwm2e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
# db = client.get_database("testdb")  # Replace "testdb" with your database name
# collection = db["items"]
db = client.get_database("student_management")
collection = db["students"]
