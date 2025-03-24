from pymongo import MongoClient
from datetime import datetime, timezone  # Import timezone for aware datetime objects

# Local MongoDB connection string (replace with Atlas URI for cloud deployment)
MONGO_URI = "mongodb://localhost:27017"

# Create a MongoDB client instance
client = MongoClient(MONGO_URI)

# Access the database named 'advent_ai_db'
db = client["advent_ai_db"]

# Access the 'books' collection within the database
books_collection = db["books"]

def save_book_metadata(filename, title=None):
    # Prepare a document with metadata about the uploaded book
    book_doc = {
        "filename": filename,
        "title": title or filename.rsplit(".", 1)[0],  # Default title: filename without extension
        "uploaded_at": datetime.now(timezone.utc)  # Store a timezone-aware UTC timestamp
    }
    # Insert the metadata document into the books collection
    books_collection.insert_one(book_doc)

def get_all_books():
    # Retrieve all book documents, excluding the internal MongoDB '_id' field
    return list(books_collection.find({}, {"_id": 0}))
