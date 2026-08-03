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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        text TEXT,
        visual INTEGER,
        kinesthetic INTEGER,
        auditory INNTEGER,
        read_write INTEGER,
        FOREIGN KEY(question_id)
            REFERENCES questions(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        tips TEXT,
        youtube_link TEXT,
        spotify_playlist TEXT,
        image
    )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answer_study_methods (
            answer_id INTEGER,
            method_id INTEGER,
            points INTEGER,
            FOREIGN KEY(answer_id)
                        REFERENCES answers(id)
            FOREIGN KEY(method_id)
                                    REFERENCES study_method(id)
        )
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating INTEGER,
        comment TEXT,
        date_posted TEXT
    )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visual INTEGER,
            auditory INTEGER,
            kinesthetic INTEGER,
            read_write INTEGER
        )
        """)

    conn.commit()
    conn.close()
