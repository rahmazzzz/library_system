from pydantic import BaseModel, Field


# ------------- PERSON ----------------
class PersonIn(BaseModel):
    name: str
    email: str


class Person(PersonIn):
    id: str = Field(alias="_id")

    model_config = {
        "validate_by_name": True
    }


# ------------- BOOK ----------------
class BookIn(BaseModel):
    title: str
    author: str
    available: bool = True


class Book(BookIn):
    id: str = Field(alias="_id")

    model_config = {
        "validate_by_name": True
    }


# ------------- BORROW ----------------
class BorrowIn(BaseModel):
    person_id: str
    book_id: str


class Borrow(BorrowIn):
    id: str = Field(alias="_id")

    model_config = {
        "validate_by_name": True
    }
