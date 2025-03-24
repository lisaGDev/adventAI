from fastapi import APIRouter, Query
from webapi.services.vectorizer import search_similar  # Function to search for similar text using vector similarity

router = APIRouter()  # Initialize API router for handling Q&A routes

@router.get("/ask")
def ask_question(question: str):
    # Use vector search to find similar content based on the question
    results = search_similar(question)
    
    # Return the matched context as a response
    return {"context": results}


@router.get("/test")
def test_search(question: str = Query(...)):
    results = search_similar(question)
    return {"top_chunks": results}