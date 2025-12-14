from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
#資料驗證模型
#PostCreate：用來接收輸入資料（POST/PUT），包含驗證規則如長度限制。 用於新增或更新書籍資料。
class BookCreate(BaseModel):#建立資料型別和規則 |後面是建立規則而none是可選欄位
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    price: int | None = Field(default=None, gt=0)#價格必須大於0
    publish_date: str | None = None
    isbn: str | None = None
    cover_url: str | None = None
#Response模型：用來回傳資料（GET），包含額外的欄位如id和created_at。 用於回應書籍資料查詢。
class BookResponse(BookCreate):#繼承BookCreate
    model_config = ConfigDict(from_attributes=True)#允許從ORM模型轉換
    id: int
    created_at: datetime#自動記錄創建時間