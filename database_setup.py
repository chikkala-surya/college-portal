import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    RollNo TEXT PRIMARY KEY,
    Name TEXT,
    Branch TEXT,
    Section TEXT,
    Mobile TEXT,
    Email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_login(
    RollNo TEXT PRIMARY KEY,
    Password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty_login(
    FacultyID TEXT PRIMARY KEY,
    Name TEXT,
    Password TEXT
)
""")

conn.commit()
conn.close()

print("Database Created")