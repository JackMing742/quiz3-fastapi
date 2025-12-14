from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel
import database
from models import BookCreate, BookResponse

app = FastAPI()#建立FastAPI


@app.get("/", response_model=dict, status_code=200)#根路由 回傳歡迎訊息
def root():
    return {"message": "AI Books API"}


@app.get("/books", response_model=list[BookResponse], status_code=200)#取得所有書籍，支援分頁並套用資料驗證回傳狀態碼
def get_books(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):#分頁參數 skip 和 limit。skip 參數表示跳過的書籍數量，用來實現分頁功能。這個參數是透過 Query 參數傳遞的，這意味著它會從 URL 查詢字串中獲取（例如：/books?skip=20）。
    try:                                                                        #limit 參數表示要返回的最大書籍數量，同樣是透過 Query 參數傳遞的。這個參數有一個限制，必須在 1 到 100 之間（包含 1 和 100）。這樣可以防止一次請求過多的資料，保護伺服器資源。
        books = database.get_all_books(skip=skip, limit=limit)
        return books
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="內部伺服器 Error")

# 取得特定書籍的詳細資訊
@app.get("/books/{book_id}", response_model=BookResponse, status_code=200)
def get_book(book_id: int):
    try:
        book = database.get_book_by_id(book_id)
        #檢查書籍是否存在
        if book is None:
            raise HTTPException(status_code=404, detail="找不到書籍")
        return book
    #回傳錯誤訊息
    except HTTPException:# 捕捉並重新引發 HTTPException，以便正確處理 404 錯誤不會被下方的 Exception 捕捉到。
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="內部伺服器 Error")

# 新增一本書籍
@app.post("/books", response_model=BookResponse, status_code=201)
def add_book(book: BookCreate = Body(...)):# 使用 Body(...) 來表示 book 參數是從請求的主體中獲取的，並且是必需的。
    try:
        #新增書籍到資料庫
        book_id = database.create_book(
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            price=book.price,
            publish_date=book.publish_date,
            isbn=book.isbn,
            cover_url=book.cover_url,
        )
        #檢查是否成功新增書籍
        if book_id == -1:
            raise HTTPException(status_code=500, detail="新增書籍失敗")
        #取得剛新增的書籍資訊並回傳
        created_book = database.get_book_by_id(book_id)
        return created_book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="內部伺服器 Error")
# 更新特定書籍的資訊
@app.put("/books/{book_id}", response_model=BookResponse, status_code=200)
def update_book(book_id: int, book: BookCreate = Body(...)):# 使用 Body(...) 來表示 book 參數是從請求的主體中獲取的，並且是必需的。
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
        #檢查是否成功更新書籍
        if not updated:
            raise HTTPException(status_code=404, detail="找不到書籍")
        #取得剛更新的書籍資訊並回傳
        updated_book = database.get_book_by_id(book_id)
        return updated_book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="內部伺服器 Error")
# 刪除特定書籍
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    try:
        deleted = database.delete_book(book_id)
        #檢查是否成功刪除書籍
        if not deleted:
            raise HTTPException(status_code=404, detail="找不到書籍")
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="內部伺服器 Error")
