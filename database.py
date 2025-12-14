import sqlite3


def get_db_connection():
    try:
        conn = sqlite3.connect("bokelai.db")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def get_all_books(skip: int, limit: int) -> list[dict]:
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (limit, skip))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return []
    finally:
        conn.close()


def get_book_by_id(book_id: int) -> dict | None:
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return None
    finally:
        conn.close()


def create_book(
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None,
) -> int:
    conn = get_db_connection()
    if conn is None:
        return -1

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, publisher, price, publish_date, isbn, cover_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (title, author, publisher, price, publish_date, isbn, cover_url),
            )
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database insertion error: {e}")
        return -1
    finally:
        conn.close()


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
                ),
            )
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database update error: {e}")
        return False
    finally:
        conn.close()


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
