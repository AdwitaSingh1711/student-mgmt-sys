from pydantic import BaseModel
from bson import ObjectId

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

    class Config:
        # This will ensure that MongoDB ObjectId can be parsed properly
        json_encoders = {
            ObjectId: str
        }