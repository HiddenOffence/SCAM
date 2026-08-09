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


def populate_answers():

    conn = get_connection()
    cursor = conn.cursor()

    answers = [

        # Question 1
        (1, "See diagrams or pictures"),
        (1, "Listen to explanations"),
        (1, "Try it myself"),
        (1, "Read instructions"),

        # Question 2
        (2, "The teacher uses slides or drawings"),
        (2, "The teacher explains verbally"),
        (2, "We do activities"),
        (2, "I take notes"),

        # Question 3
        (3, "Picture it in my mind"),
        (3, "Say it in my head"),
        (3, "Practice again"),
        (3, "Re-read it"),

        # Question 4
        (4, "Colors and diagrams"),
        (4, "Key phrases"),
        (4, "Examples"),
        (4, "Full sentences"),

        # Question 5
        (5, "Highlight and draw"),
        (5, "Talk out loud"),
        (5, "Move around"),
        (5, "Read quietly"),

        # Question 6
        (6, "I see it"),
        (6, "I hear it"),
        (6, "I do it"),
        (6, "I write it"),

        # Question 7
        (7, "There are no visuals"),
        (7, "Nobody explains"),
        (7, "I don't practice"),
        (7, "I don't review notes"),

        # Question 8
        (8, "Diagrams"),
        (8, "Saying them aloud"),
        (8, "Using examples"),
        (8, "Writing them"),

        # Question 9
        (9, "Look at summaries"),
        (9, "Explain topics aloud"),
        (9, "Practice questions"),
        (9, "Read notes"),

        # Question 10
        (10, "I can see patterns"),
        (10, "Someone teaches me"),
        (10, "I experiment"),
        (10, "I read"),

        # Question 11
        (11, "With visual tools"),
        (11, "With someone"),
        (11, "Hands-on"),
        (11, "Alone"),

        # Question 12
        (12, "Mindmaps"),
        (12, "Discussion"),
        (12, "Activities"),
        (12, "Reading"),

        # Question 13
        (13, "Draw it out"),
        (13, "Ask someone"),
        (13, "Try different ways"),
        (13, "Check notes"),

        # Question 14
        (14, "See diagrams"),
        (14, "Listen"),
        (14, "Build or test"),
        (14, "Read"),

        # Question 15
        (15, "It's boring visually"),
        (15, "It's silent"),
        (15, "I'm sitting too long"),
        (15, "It's confusing"),

        # Question 16
        (16, "Work looks organized"),
        (16, "Someone encourages me"),
        (16, "I see progress"),
        (16, "I understand it"),

        # Question 17
        (17, "Visual"),
        (17, "Spoken"),
        (17, "Demonstrated"),
        (17, "Written"),

        # Question 18
        (18, "It looks neat"),
        (18, "I can talk"),
        (18, "It's interactive"),
        (18, "It's clear"),

        # Question 19
        (19, "Videos"),
        (19, "Podcasts"),
        (19, "Experiments"),
        (19, "Books"),

        # Question 20
        (20, "My notes look good"),
        (20, "There is background sound"),
        (20, "I take breaks"),
        (20, "It's quiet"),

        # Question 21
        (21, "Highlighting"),
        (21, "Explaining"),
        (21, "Practicing"),
        (21, "Reading"),

        # Question 22
        (22, "Use colors"),
        (22, "Say things aloud"),
        (22, "Solve problems"),
        (22, "Re-read"),

        # Question 23
        (23, "Can visualize it"),
        (23, "Can explain it"),
        (23, "Can do it"),
        (23, "Can describe it"),

        # Question 24
        (24, "Find diagrams"),
        (24, "Watch videos"),
        (24, "Try questions"),
        (24, "Read textbook"),

        # Question 25
        (25, "Visual ideas"),
        (25, "Listening"),
        (25, "Practical work"),
        (25, "Reading"),

        # Question 26
        (26, "Notes look messy"),
        (26, "It's too quiet"),
        (26, "I sit too long"),
        (26, "Text is long"),

        # Question 27
        (27, "Colorful"),
        (27, "Spoken"),
        (27, "Active"),
        (27, "Written"),

        # Question 28
        (28, "See summaries"),
        (28, "Explain topics"),
        (28, "Practice questions"),
        (28, "Review notes"),

        # Question 29
        (29, "Plain text"),
        (29, "Silent reading"),
        (29, "Sitting still"),
        (29, "Long explanations"),

        # Question 30
        (30, "See it"),
        (30, "Hear it"),
        (30, "Do it"),
        (30, "Read it")
    ]

    cursor.executemany("""
        INSERT INTO answers
        (question_id, text)
        VALUES (?, ?)
    """, answers)

    conn.commit()
    conn.close()


def populate_answer_study_methods():

    conn = get_connection()
    cursor = conn.cursor()

    # Study method IDs
    VISUAL = 1
    AUDITORY = 2
    KINESTHETIC = 3
    READ_WRITE = 4

    relationships = []

    # Every question has:
    # A = Visual
    # B = Auditory
    # C = Kinesthetic
    # D = Read/Write

    for question_id in range(1, 31):

        first_answer_id = (question_id - 1) * 4 + 1

        relationships.append(
            (first_answer_id, VISUAL, 1)
        )

        relationships.append(
            (first_answer_id + 1, AUDITORY, 1)
        )

        relationships.append(
            (first_answer_id + 2, KINESTHETIC, 1)
        )

        relationships.append(
            (first_answer_id + 3, READ_WRITE, 1)
        )

    cursor.executemany("""
        INSERT OR IGNORE INTO answer_study_methods
        (answer_id, method_id, points)
        VALUES (?, ?, ?)
    """, relationships)

    conn.commit()
    conn.close()
