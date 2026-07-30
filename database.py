import sqlite3,
from database import create_tables

DATABASE = "database/quiz.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL,
        category TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        answer_text TEXT,
        study_method TEXT,
        FOREIGN KEY(question_id)
            REFERENCES questions(question_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_methods (
        method_id INTEGER PRIMARY KEY AUTOINCREMENT,
        method_name TEXT,
        description TEXT,
        youtube_link TEXT,
        spotify_playlist TEXT,
        image TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        rating INTEGER,
        comment TEXT,
        date_posted TEXT
    )
    """)

    conn.commit()
    conn.close()
