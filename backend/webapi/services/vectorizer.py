from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from webapi.services.processor import chunk_text  # Function to split text into overlapping chunks

# Load a pre-trained sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set the embedding dimension for the FAISS index (must match model output)
dimension = 384

# Create a FAISS index for fast similarity search using L2 (Euclidean) distance
index = faiss.IndexFlatL2(dimension)

# In-memory storage of text chunks for retrieval based on search results
stored_chunks = []

def index_text(text):
    global stored_chunks

    # Break text into overlapping chunks
    chunks = chunk_text(text)

    # Add chunks to in-memory store for later retrieval
    stored_chunks.extend(chunks)

    # Encode chunks into vector embeddings
    embeddings = model.encode(chunks)

    # Add embeddings to the FAISS index
    index.add(np.array(embeddings))

def search_similar(question, k=3):
    # Encode the input question into a vector
    question_embedding = model.encode([question])

    # Search the FAISS index for the top-k most similar chunks
    distances, indices = index.search(np.array(question_embedding), k)

    # Retrieve and return the matching text chunks
    return [stored_chunks[i] for i in indices[0]]
