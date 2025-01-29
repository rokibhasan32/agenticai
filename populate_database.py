import sqlite3
import random
from faker import Faker

fake = Faker()

# Sample genres and authors
GENRES = ["Fiction", "Non-fiction", "Science", "Philosophy", "Fantasy", "History", "Mystery"]
AUTHORS = ["J.K. Rowling", "George Orwell", "Isaac Asimov", "Jane Austen", "Stephen King"]

def populate_database():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    # Insert random books
    for _ in range(20):
        title = fake.sentence(nb_words=3)
        author = random.choice(AUTHORS)
        genre = random.choice(GENRES)
        published_year = random.randint(1900, 2023)
        cursor.execute("""
        INSERT INTO Books (title, author, genre, published_year) 
        VALUES (?, ?, ?, ?)""", (title, author, genre, published_year))

    # Insert random students
    for _ in range(10):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        cursor.execute("""
        INSERT INTO Students (name, email, phone) 
        VALUES (?, ?, ?)""", (name, email, phone))

    # Add some borrowed books
    for _ in range(5):
        student_id = random.randint(1, 10)
        book_id = random.randint(1, 20)
        borrowed_date = fake.date_this_year()
        return_date = fake.date_between(start_date=borrowed_date, end_date="+30d")
        cursor.execute("""
        INSERT INTO BorrowedBooks (student_id, book_id, borrowed_date, return_date) 
        VALUES (?, ?, ?, ?)""", (student_id, book_id, borrowed_date, return_date))

    conn.commit()
    conn.close()
    print("Database populated with sample data!")

if __name__ == "__main__":
    populate_database()
