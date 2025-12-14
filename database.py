import sqlite3

#連線到SQLite資料庫
def get_db_connection():
    try:
        conn = sqlite3.connect("bokelai.db")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

#取得所有書籍資料
def get_all_books(skip: int, limit: int) -> list[dict]:
    conn = get_db_connection()
    #如果連線失敗，回傳空列表
    if conn is None:
        return []
    #回傳查詢結果
    try:
        with conn:
            cursor = conn.cursor()                                                  #創建了一個資料庫操作游標，用來執行 SQL 查詢。
            cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (limit, skip))
            #LIMIT: 用來指定查詢結果中返回的最大紀錄數量。這是控制返回資料量的一種方式。OFFSET: 用來指定查詢從哪一條紀錄開始返回。這通常和 LIMIT 一起使用，來實現 分頁查詢。
            #QL 查詢中使用 ? 來代替實際的變數值，這是一種參數化查詢的寫法。這裡的 ? 會被 limit 和 skip 替代，這樣可以控制返回的紀錄數量及跳過的紀錄數量。
            rows = cursor.fetchall()                                                #執行查詢後，使用 fetchall() 方法取回所有的結果行，結果會被儲存在 rows 變數中
            return [dict(row) for row in rows]#將每一行結果轉換為字典，並返回包含這些字典的列表
    #回報錯誤訊息
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return []
    #手動關閉連線
    finally:
        conn.close()

#根據ID取得單一書籍資料
def get_book_by_id(book_id: int) -> dict | None:
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))#WHERE 子句用來過濾資料，僅返回符合條件的紀錄。在這裡，條件是 id = ?，也就是根據 id 欄位的值來過濾資料。
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return None
    finally:
        conn.close()

#新增書籍資料
def create_book(
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None,
) -> int: #上述是函式的參數列表，定義了新增書籍所需的各個欄位資訊。函式的返回值類型是 int，表示新增書籍後會回傳該書籍的唯一識別碼（ID）。
    conn = get_db_connection()
    if conn is None:
        return -1

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, publisher, price, publish_date, isbn, cover_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (title, author, publisher, price, publish_date, isbn, cover_url),
            )#INSERT INTO books: 這是 SQL 的插入語法，表示將一條新的紀錄插入到 books 資料表中。最後是參數是要插入的值，這些值會依序對應到前面指定的欄位。
            return cursor.lastrowid #cursor.lastrowid 是一個游標屬性，它返回最近一次插入操作所生成的 自增 ID
    except sqlite3.Error as e:
        print(f"Database insertion error: {e}")
        return -1
    finally:
        conn.close()

#更新書籍資料
def update_book(
    book_id: int,
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None,
) -> bool:
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE books SET title = ?, author = ?, publisher = ?, price = ?, publish_date = ?, isbn = ?, cover_url = ? WHERE id = ?",
                (
                    title,
                    author,
                    publisher,
                    price,
                    publish_date,
                    isbn,
                    cover_url,
                    book_id,
                ),#WHERE 子句用來指定要更新哪一條紀錄。在這裡，條件是 id = ?，也就是根據 id 欄位的值來定位要更新的書籍紀錄。
            )
            return cursor.rowcount > 0 #cursor.rowcount 是一個游標屬性，它返回最近一次執行的 SQL 語句所影響的行數。在這裡，我們用它來判斷更新操作是否成功。如果 rowcount 大於 0，表示有行被更新，函式就回傳 True；否則回傳 False。
    except sqlite3.Error as e:
        print(f"Database update error: {e}")
        return False
    finally:
        conn.close()

#刪除書籍資料
def delete_book(book_id: int) -> bool:
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database deletion error: {e}")
        return False
    finally:
        conn.close()
