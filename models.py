from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
class BookCreate(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    price: int | None = Field(default=None, gt=0)
    publish_date: str | None = None
    isbn: str | None = None
    cover_url: str | None = None
class BookResponse(BookCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime