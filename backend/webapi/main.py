from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webapi.routes import books, qa

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(books.router, prefix="/books")
app.include_router(qa.router, prefix="/qa")