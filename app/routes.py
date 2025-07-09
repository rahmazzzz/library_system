from fastapi import APIRouter, HTTPException
from .database import people_collection, books_collection, borrow_collection
from .schemas import Person, Book, Borrow
from bson import ObjectId

router = APIRouter()

# ---------------- People ----------------
@router.post("/people")
async def add_person(person: Person):
    person_dict = person.dict()
    result = await people_collection.insert_one(person_dict)
    return {"_id": str(result.inserted_id), **person_dict}

@router.get("/people")
async def get_people():
    people = []
    async for p in people_collection.find():
        p["_id"] = str(p["_id"])
        people.append(p)
    return people

# ---------------- Books ----------------
@router.post("/books")
async def add_book(book: Book):
    book_dict = book.dict()
    result = await books_collection.insert_one(book_dict)
    return {"_id": str(result.inserted_id), **book_dict}

@router.get("/books")
async def get_books():
    books = []
    async for b in books_collection.find():
        b["_id"] = str(b["_id"])
        books.append(b)
    return books

# ---------------- Borrow ----------------
@router.post("/borrow")
async def borrow_book(borrow: Borrow):
    # Check if person exists
    person = await people_collection.find_one({"_id": ObjectId(borrow.person_id)})
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # Check if book exists
    book = await books_collection.find_one({"_id": ObjectId(borrow.book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.get("available", True):
        raise HTTPException(status_code=400, detail="Book not available")

    # Mark book as not available
    await books_collection.update_one(
        {"_id": ObjectId(borrow.book_id)},
        {"$set": {"available": False}}
    )

    # Create borrow record
    borrow_dict = borrow.dict()
    result = await borrow_collection.insert_one(borrow_dict)
    return {"_id": str(result.inserted_id), **borrow_dict}

@router.get("/borrow")
async def get_borrow_records():
    records = []
    async for record in borrow_collection.find():
        record["_id"] = str(record["_id"])
        records.append(record)
    return records
