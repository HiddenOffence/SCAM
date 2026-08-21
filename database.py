import sqlite3

DATABASE = "database/quiz.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    # Make sure foreign keys are enforced
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def get_sections():
    conn = get_connection()

    sections = conn.execute("""
        SELECT id, name, description
        FROM sections
        ORDER BY id
    """).fetchall()

    conn.close()

    return sections


def get_questions_by_section(section_id):
    conn = get_connection()

    questions = conn.execute("""
        SELECT id, section_id, question_text
        FROM questions
        WHERE section_id = ?
        ORDER BY id
    """, (section_id,)).fetchall()

    conn.close()

    return questions


def get_answers_by_question(question_id):
    conn = get_connection()

    answers = conn.execute("""
        SELECT id, question_id, text
        FROM answers
        WHERE question_id = ?
        ORDER BY id
    """, (question_id,)).fetchall()

    conn.close()

    return answers


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Quiz sections
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)

    # Questions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,

        FOREIGN KEY (section_id)
            REFERENCES sections(id)
    )
    """)

    # Answers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    text TEXT NOT NULL,

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

    conn.commit()
    conn.close()

    def calculate_quiz_results(answer_ids):
        conn = get_connection()

        scores = conn.execute("""
            SELECT
                study_methods.id,
                study_methods.name,
                study_methods.description,
                study_methods.tips,
                study_methods.youtube_link,
                study_methods.spotify_playlist,
                study_methods.image,
                SUM(answer_study_methods.points) AS score

            FROM answer_study_methods

            JOIN study_methods
                ON answer_study_methods.method_id = study_methods.id

            WHERE answer_study_methods.answer_id
                IN ({placeholders})

            GROUP BY study_methods.id

            ORDER BY score DESC
        """.format(
            placeholders=",".join("?" * len(answer_ids))
        ), answer_ids).fetchall()

        conn.close()

        return scores
