import motor.motor_asyncio
import os
from dotenv import load_dotenv

# Load your .env file (named code.env)
load_dotenv("code.env")

MONGO_DETAILS = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client[DATABASE_NAME]

# Define your collections
people_collection = database.get_collection("people")
books_collection = database.get_collection("books")
borrow_collection = database.get_collection("borrow")

