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


def populate_study_methods():

    conn = get_connection()
    cursor = conn.cursor()

    methods = [
        (
            "Visual",
            "You may benefit from learning through diagrams, images, colours, charts and visual organisation.",
            "Try diagrams, mind maps, colour coding, videos and visual summaries.",
            "",
            "",
            ""
        ),

        (
            "Auditory",
            "You may benefit from learning through listening, explaining ideas and discussing information.",
            "Try explaining concepts aloud, discussing ideas with others and using spoken summaries.",
            "",
            "",
            ""
        ),

        (
            "Kinesthetic",
            "You may benefit from active, practical and hands-on approaches to learning.",
            "Try practice activities, demonstrations, experiments and learning by doing.",
            "",
            "",
            ""
        ),

        (
            "Read/Write",
            "You may benefit from learning through reading, writing and organising information in words.",
            "Try written summaries, notes, lists, flashcards and practice questions.",
            "",
            "",
            ""
        )
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO study_methods
        (
            name,
            description,
            tips,
            youtube_link,
            spotify_playlist,
            image
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, methods)

    conn.commit()
    conn.close()


def populate_sections():

    conn = get_connection()
    cursor = conn.cursor()

    sections = [
        (
            "Learning Style",
            "Explore how you prefer to receive and understand new information."
        ),
        (
            "Memory Habits",
            "Explore how you remember and revise information."
        ),
        (
            "Study Preferences",
            "Explore the types of study activities and environments you prefer."
        ),
        (
            "Motivation",
            "Explore what helps you stay motivated while studying."
        ),
        (
            "Study Behaviour",
            "Explore how you currently approach studying and revision."
        ),
        (
            "Focus & Habits",
            "Explore the habits and conditions that affect your concentration."
        )
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO sections
        (name, description)
        VALUES (?, ?)
    """, sections)

    conn.commit()
    conn.close()


def populate_questions():

    conn = get_connection()
    cursor = conn.cursor()

    questions = [

        # Learning Style
        (1, "When learning something new, I prefer to:"),
        (1, "In class I remember best when:"),
        (1, "If I forget something, I usually:"),
        (1, "My notes usually include:"),
        (1, "When studying, I like to:"),

        # Memory Habits
        (2, "I remember information best when:"),
        (2, "I usually forget things when:"),
        (2, "The easiest way for me to learn definitions is:"),
        (2, "Before a test I usually:"),
        (2, "I learn fastest when:"),

        # Study Preferences
        (3, "I prefer studying:"),
        (3, "My ideal study session includes:"),
        (3, "When homework is hard I:"),
        (3, "I enjoy subjects where I:"),
        (3, "I lose focus when:"),

        # Motivation
        (4, "I stay motivated when:"),
        (4, "I prefer instructions that are:"),
        (4, "I like studying when:"),
        (4, "I enjoy learning through:"),
        (4, "I focus best when:"),

        # Study Behaviour
        (5, "I usually study by:"),
        (5, "When revising I:"),
        (5, "When I understand something I:"),
        (5, "If a topic is confusing I:"),
        (5, "My best school subjects involve:"),

        # Focus & Habits
        (6, "I get distracted when:"),
        (6, "I prefer revision that is:"),
        (6, "I feel confident when I:"),
        (6, "The hardest studying for me is:"),
        (6, "I think studying works best when I:")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO questions
        (section_id, question_text)
        VALUES (?, ?)
    """, questions)

    conn.commit()
    conn.close()
