from fastapi import APIRouter, UploadFile, File
from webapi.services.processor import extract_text_from_pdf
from webapi.services.vectorizer import index_text
from webapi.db import save_book_metadata, get_all_books
import os

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Ensure 'books' directory exists
    os.makedirs("books", exist_ok=True)
    file_path = f"books/{file.filename}"

    # Save the uploaded file to disk
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Save the filename metadata (e.g., to MongoDB)
    save_book_metadata(filename=file.filename)

    # Extract text from the PDF
    text = extract_text_from_pdf(file_path)

    # Index the extracted text for search
    index_text(text)

    return {"message": f"{file.filename} uploaded and processed"}

@router.get("/")
def list_books():
    # Retrieve all uploaded book metadata
    books = get_all_books()
    return {"books": books}
