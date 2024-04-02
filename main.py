import math
import random

from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB connection
MONGO_URL = 'mongodb://pythonfastapidb:27017'  # Update the hostname to match the service name
client = AsyncIOMotorClient(MONGO_URL)
db = client['pythonapidb']
collection = db['names']

# Model


class Person(BaseModel):
    name: str


@app.get("/")
async def read_root():
    return {"Hello": "Welcome to the fastAPI"}


@app.get("/names", response_model=list[Person])
async def get_names():
    documents = []
    cursor = collection.find({})
    async for document in cursor:
        documents.append(document)
    return documents


@app.post("/names", response_model=Person)
async def post_name(person: Person):
    result = await collection.insert_one(person.dict())
    return person


@app.put("/names/{name}", response_model=Person)
async def update_name(name: str, person: Person):
    updated_person = await collection.find_one_and_update({"name": name}, {"$set": person.dict()})
    if updated_person:
        return person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Name {name} not found")


@app.delete("/names/{name}", response_model=Person)
async def delete_name(name: str):
    deleted_person = await collection.find_one_and_delete({"name": name})
    if deleted_person:
        return deleted_person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Name {name} not found")


@app.post("/calculate_sin")
async def calculate_sin(number: float):
    return math.sin(number)


@app.post("/calculate_cos")
async def calculate_cos(number: float):
    return math.cos(number)


@app.post("/generate_random_number")
async def random_number():
    random_number = random.randint(0, 100)
    return round(random_number)
