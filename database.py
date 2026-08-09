import sqlite3

DATABASE = "database/quiz.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    # Make sure foreign keys are enforced
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Questions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL
    )
    """)

    # Answers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        visual INTEGER DEFAULT 0,
        kinesthetic INTEGER DEFAULT 0,
        auditory INTEGER DEFAULT 0,
        read_write INTEGER DEFAULT 0,

        FOREIGN KEY (question_id)
            REFERENCES questions(id)
    )
    """)

    # Study methods
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        tips TEXT,
        youtube_link TEXT,
        spotify_playlist TEXT,
        image TEXT
    )
    """)

    # Many-to-many relationship
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answer_study_methods (
        answer_id INTEGER NOT NULL,
        method_id INTEGER NOT NULL,
        points INTEGER DEFAULT 0,

        PRIMARY KEY (answer_id, method_id),

        FOREIGN KEY (answer_id)
            REFERENCES answers(id),

        FOREIGN KEY (method_id)
            REFERENCES study_methods(id)
    )
    """)

    # Reviews
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT NOT NULL,
        date_posted TEXT NOT NULL
    )
    """)

    # Results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visual INTEGER DEFAULT 0,
        auditory INTEGER DEFAULT 0,
        kinesthetic INTEGER DEFAULT 0,
        read_write INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
