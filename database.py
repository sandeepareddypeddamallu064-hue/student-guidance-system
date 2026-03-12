import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    gpa REAL,
    coding INTEGER,
    ml_skill INTEGER,
    internship INTEGER
)
""")

conn.commit()
conn.close()

print("Database created")