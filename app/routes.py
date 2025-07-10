from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId

from .database import people_collection, books_collection, borrow_collection
from .schemas import Person, PersonIn, Book, BookIn, Borrow, BorrowIn

router = APIRouter()


# --------- Helpers ---------
def person_helper(person) -> dict:
    return {
        "_id": str(person["_id"]),
        "name": person["name"],
        "email": person["email"]
    }


def book_helper(book) -> dict:
    return {
        "_id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "available": book.get("available", True)
    }


def borrow_helper(borrow) -> dict:
    return {
        "_id": str(borrow["_id"]),
        "person_id": str(borrow["person_id"]),
        "book_id": str(borrow["book_id"])
    }


# --------- PEOPLE ---------
@router.post("/people", response_model=Person)
async def add_person(person: PersonIn):
    person_dict = person.dict()
    result = await people_collection.insert_one(person_dict)
    new_person = await people_collection.find_one({"_id": result.inserted_id})
    return person_helper(new_person)


@router.get("/people", response_model=List[Person])
async def get_people():
    people = []
    async for p in people_collection.find():
        people.append(person_helper(p))
    return people


# --------- BOOKS ---------
@router.post("/books", response_model=Book)
async def add_book(book: BookIn):
    book_dict = book.dict()
    result = await books_collection.insert_one(book_dict)
    new_book = await books_collection.find_one({"_id": result.inserted_id})
    return book_helper(new_book)


@router.get("/books", response_model=List[Book])
async def get_books():
    books = []
    async for b in books_collection.find():
        books.append(book_helper(b))
    return books


# --------- BORROWS ---------
@router.post("/borrows", response_model=Borrow)
async def borrow_book(borrow: BorrowIn):
    # Check if person exists
    person = await people_collection.find_one({"_id": ObjectId(borrow.person_id)})
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # Check if book exists and is available
    book = await books_collection.find_one({"_id": ObjectId(borrow.book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.get("available", True):
        raise HTTPException(status_code=400, detail="Book not available")

    # Mark book as unavailable
    await books_collection.update_one(
        {"_id": ObjectId(borrow.book_id)},
        {"$set": {"available": False}}
    )

    # Insert borrow record with ObjectId references
    borrow_doc = {
        "person_id": ObjectId(borrow.person_id),
        "book_id": ObjectId(borrow.book_id)
    }
    result = await borrow_collection.insert_one(borrow_doc)
    new_borrow = await borrow_collection.find_one({"_id": result.inserted_id})
    return borrow_helper(new_borrow)


@router.get("/borrows", response_model=List[Borrow])
async def get_borrow_records():
    records = []
    async for record in borrow_collection.find():
        records.append(borrow_helper(record))
    return records
