import sqlite3

def create_database():
    # Connect to SQLite (creates the file if it doesn't exist)
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    # Create Books table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        published_year INTEGER,
        available INTEGER DEFAULT 1
    )
    """)

    # Create Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT
    )
    """)

    # Create BorrowedBooks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BorrowedBooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        borrowed_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY(student_id) REFERENCES Students(id),
        FOREIGN KEY(book_id) REFERENCES Books(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database and tables created successfully!")

if __name__ == "__main__":
    create_database()
