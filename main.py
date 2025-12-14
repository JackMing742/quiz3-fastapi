from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel
import database
from models import BookCreate, BookResponse

app = FastAPI()


@app.get("/", response_model=dict, status_code=200)
def root():
    return {"message": "AI Books API"}


@app.get("/books", response_model=list[BookResponse], status_code=200)
def get_books(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    try:
        books = database.get_all_books(skip=skip, limit=limit)
        return books
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/books/{book_id}", response_model=BookResponse, status_code=200)
def get_book(book_id: int):
    try:
        book = database.get_book_by_id(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/books", response_model=BookResponse, status_code=201)
def add_book(book: BookCreate = Body(...)):
    try:
        book_id = database.create_book(
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            price=book.price,
            publish_date=book.publish_date,
            isbn=book.isbn,
            cover_url=book.cover_url,
        )
        if book_id == -1:
            raise HTTPException(status_code=500, detail="Failed to create book")
        created_book = database.get_book_by_id(book_id)
        return created_book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/books/{book_id}", response_model=BookResponse, status_code=200)
def update_book(book_id: int, book: BookCreate = Body(...)):
    try:
        updated = database.update_book(
            book_id=book_id,
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            price=book.price,
            publish_date=book.publish_date,
            isbn=book.isbn,
            cover_url=book.cover_url,
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Book not found")
        updated_book = database.get_book_by_id(book_id)
        return updated_book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    try:
        deleted = database.delete_book(book_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Book not found")
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
