from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Person(BaseModel):
    name: str
    email: str

class Book(BaseModel):
    title: str
    author: str
    available: bool = True

class Borrow(BaseModel):
    person_id: str  # store as string, convert to ObjectId when querying
    book_id: str