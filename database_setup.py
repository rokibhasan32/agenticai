# database_setup.py
import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker and database
fake = Faker()
DATABASE_NAME = "library.db"

def create_database():
    """Create database tables with proper schema"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create Books table with additional agentic fields
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        published_year INTEGER,
        available INTEGER DEFAULT 1,
        shelf_location TEXT,
        prerequisites TEXT,
        summary TEXT
    )
    ''')

    # Create Students table with university-specific fields
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        department TEXT
    )
    ''')

    # Create BorrowedBooks table with renewal tracking
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BorrowedBooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        borrowed_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        renewals_left INTEGER DEFAULT 2,
        FOREIGN KEY(student_id) REFERENCES Students(id),
        FOREIGN KEY(book_id) REFERENCES Books(id)
    )
    ''')

    conn.commit()
    conn.close()

def populate_data():
    """Populate tables with realistic random data"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Configuration
    NUM_BOOKS = 200
    NUM_STUDENTS = 100
    NUM_BORROWED = 150

    # Academic departments and book genres
    DEPARTMENTS = ["Computer Science", "Electrical Engineering", "Business Administration", 
                  "English Literature", "Physics", "Mathematics", "Philosophy"]
    GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Technology", 
             "Philosophy", "Mathematics", "Literature", "Art", "Business"]

    # Generate Books
    print("Generating books...")
    for _ in range(NUM_BOOKS):
        book_data = (
            fake.catch_phrase().title(),  # Book title
            fake.name(),                  # Author name
            random.choice(GENRES),
            random.randint(1900, 2023),
            random.choice([0, 1]),        # Availability
            f"Shelf {random.choice(['A','B','C'])}-{random.randint(1, 50)}",
            random.choice(["None", "Basic Mathematics", "Intro to Programming", 
                          "Literature 101", "Physics Fundamentals"]),
            fake.paragraph(nb_sentences=3) # Book summary
        )
        cursor.execute('''
            INSERT INTO Books 
            (title, author, genre, published_year, available, shelf_location, prerequisites, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', book_data)

    # Generate Students
    print("Generating students...")
    for _ in range(NUM_STUDENTS):
        student_data = (
            f"DIU-{random.randint(2020, 2024)}-{random.randint(1000, 9999)}",
            fake.name(),
            fake.email(),
            fake.phone_number(),
            random.choice(DEPARTMENTS)
        )
        cursor.execute('''
            INSERT INTO Students 
            (student_id, name, email, phone, department)
            VALUES (?, ?, ?, ?, ?)
        ''', student_data)

    # Generate Borrowing Records
    print("Generating borrowing records...")
    for _ in range(NUM_BORROWED):
        student_id = random.randint(1, NUM_STUDENTS)
        book_id = random.randint(1, NUM_BOOKS)
        borrowed_date = fake.date_between(start_date='-1year', end_date='today')
        due_date = borrowed_date + timedelta(days=14)
        
        cursor.execute('''
            INSERT INTO BorrowedBooks 
            (student_id, book_id, borrowed_date, due_date, renewals_left)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            student_id,
            book_id,
            borrowed_date.isoformat(),
            due_date.isoformat(),
            random.randint(0, 2)  # Number of remaining renewals
        ))
        
        # Update book availability
        cursor.execute('''
            UPDATE Books SET available = 0 WHERE id = ?
        ''', (book_id,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Creating database structure...")
    create_database()
    print("Populating with sample data...")
    populate_data()
    print(f"Database {DATABASE_NAME} created and populated successfully!")
    print(f"Generated: 200 books, 100 students, 150 borrowing records")