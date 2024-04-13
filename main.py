from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import helper

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    isbn: str
    id: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Book Management API"}

@app.get("/books")
def get_books():
    """Endpoint to retrieve all books."""
    return helper.load_books()

@app.post("/books", response_model=Book, status_code=201)
def add_a_book(book: Book):
    """Endpoint to add a new book."""
    ## Add the book to the database
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """Endpoint to delete a book by ID."""
    #ADD CODE HERE
    if len(books) == len(new_books):
        raise HTTPException(status_code=404, detail="Book not found")
    #save the books
    return {"message": "Book deleted successfully"}

