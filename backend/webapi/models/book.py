from fastapi import APIRouter, UploadFile, File
from webapi.services.processor import extract_text_from_pdf  # Function to extract text from a PDF file
from webapi.services.vectorizer import index_text  # Function to index extracted text (e.g., for vector search)
from webapi.db import save_book_metadata, get_all_books  # Functions to interact with book metadata storage
import os

router = APIRouter()  # Initialize API router for handling routes related to books

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Create 'books' directory if it doesn't exist
    os.makedirs("books", exist_ok=True)
    
    # Define the path to save the uploaded PDF
    file_path = f"books/{file.filename}"

    # Save the uploaded file to disk
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Save the filename as metadata to the database
    save_book_metadata(filename=file.filename)

    # Extract text from the saved PDF
    text = extract_text_from_pdf(file_path)

    # Index the extracted text for search or retrieval
    index_text(text)

    # Return a success message
    return {"message": f"{file.filename} uploaded and processed"}

@router.get("/")
def list_books():
    # Retrieve all book metadata from the database
    books = get_all_books()
    
    # Return the list of books
    return {"books": books}
