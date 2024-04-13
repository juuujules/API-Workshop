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
    helper.add_book(book.dict())
    return book

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """Endpoint to retrieve a specific book by its ID."""
    books = helper.load_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    """Endpoint to update an existing book."""
    books = helper.load_books()
    index = next((i for i, b in enumerate(books) if b['id'] == book_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = book.dict()
    updated_book['id'] = book_id
    books[index] = updated_book
    helper.save_books(books)
    return updated_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """Endpoint to delete a book by ID."""
    books = helper.load_books()
    new_books = [b for b in books if b['id'] != book_id]
    if len(books) == len(new_books):
        raise HTTPException(status_code=404, detail="Book not found")
    helper.save_books(new_books)
    return {"message": "Book deleted successfully"}

