from fastapi import APIRouter, HTTPException, status, Query
from app.models import Student
from app.database import db,collection  # Import from database module
from fastapi import HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from typing import Optional

router = APIRouter()

@router.post("/students", status_code=status.HTTP_201_CREATED, summary="Create Students")
async def create_student(student: Student):
    """
    Create a student in database.
    
    - example schema
    
    Returns:
    - HTTP 204 on successful creation.
    """
    student_dict = student.dict()
    result = await collection.insert_one(student_dict)
    
    student_dict["_id"] = str(result.inserted_id)
    
    # return {"id": str(result.inserted_id), "student": student_dict}
    return {"id": str(result.inserted_id)}



@router.get("/students", summary="List Students")
async def get_students(
    country: Optional[str] = Query(None, description="Filter by country"),
    age: Optional[int] = Query(None, description="Filter by minimum age")
):
    """
    Fetch a list of students from the database based on filters
    
    - `country`: Filter studentss by their country of origin (case-sensitive).
    - `age`: Only include students older than mentioned age.
    """
    query = {}

    if country:
        query["address.country"] = country
    
    if age is not None:
        query["age"] = {"$gte": age}

    # Fetch matching items from the database
    students = await collection.find(query, {"name": 1, "age": 1, "_id": 0}).to_list(length=100)
    
    # Return the response
    return {"data": students}


@router.get("/students/{item_id}", summary="Fetch student")
async def get_student(item_id: str):

    """
    Fetch student from the database by it's id
    
    - `item_id`: The ID of the student item to be updated (required).
    """
    try:
        # Convert string `item_id` to ObjectId
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item_id format")
    
    student = await collection.find_one({"_id": object_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Manually convert ObjectId to string
    student["_id"] = str(student["_id"])
    
    # Ensure that the response is JSON serializable
    return jsonable_encoder(student)



@router.patch("/students/{item_id}", summary="Update student", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(item_id: str, updates: dict):
    """
    Update properties of a student item in the database.
    
    - `item_id`: The ID of the student item to be updated (required).
    - `updates`: A dictionary of fields to update (optional).
    
    Returns:
    - HTTP 204 No Content on success.
    - Raises HTTP 404 if the item is not found.
    """
    # Validate `item_id`
    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item_id format")
    
    # Remove `_id` from updates to prevent conflicts
    if "_id" in updates:
        del updates["_id"]

    # Perform the update in MongoDB
    result = await collection.update_one({"_id": object_id}, {"$set": updates})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Return 204 No Content on success
    # return {"status_code": 204, "message": "Update successful!"}
    return {}

@router.delete("/students/{item_id}", summary="Delete student")
async def delete_student(item_id: str):
    """
    Delete an item from the database using its `item_id`.
    
    - `item_id`: The ID of the item to be deleted (required).
    
    Returns:
    - HTTP 200 on successful deletion.
    - Raises HTTP 404 if the item is not found.
    """
    # Validate `item_id`
    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item_id format")
    
    # Perform the delete operation in MongoDB
    result = await collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Return a success response
    return {"status_code": 200, "message": "Item deleted successfully!"}
