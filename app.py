from flask import Flask, request
from uuid import uuid1
from db import Connection
from models.user_model import User  # Import the User model
from pydantic import ValidationError

app = Flask(__name__)
db = Connection('flask_mongo_crud')

@app.post("/user")
def insert_user():
    try:
        # Parse and validate request data
        user_data = User(**request.json)

        # with model 
        # user_data = dict(request.json)

        # Generate a unique ID
        _id = str(uuid1().hex)
        user_dict = user_data.dict()
        user_dict.update({"_id": _id})

        # Insert into database
        result = db.user.insert_one(user_dict)
        if not result.inserted_id:
            return {"message": "Failed to insert"}, 500

        return {
            "message": "Success",
            "data": {
                "user": str(result.inserted_id)
            }
        }, 200
    except ValidationError as e:
        # Return validation errors
        return {"message": "Validation failed", "errors": e.errors()}, 400


@app.get("/user/<user_id>/")
def get_user(user_id):
    query = {
        "_id": user_id
    }
    user = db.user.find_one(query)

    if not user:
        return {
            "message": "User is not found"
        }, 404

    return {
        "data": user
    }, 200


@app.delete("/user/<user_id>/")
def delete_user(user_id):
    query = {
        "_id": user_id
    }
    result = db.user.delete_one(query)

    if not result.deleted_count:
        return {
            "message": "Failed to delete"
        }, 500

    return {"message": "Delete success"}, 200


@app.put("/user/<user_id>/")
def update_user(user_id):
    query = {
        "_id": user_id
    }
    content = {"$set": dict(request.json)}
    result = db.user.update_one(query, content)

    if not result.matched_count:
        return {
            "message": "Failed to update. Record is not found"
        }, 404

    if not result.modified_count:
        return {
            "message": "No changes applied"
        }, 500

    return {"message": "Update success"}, 200
