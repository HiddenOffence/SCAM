from flask import Flask, render_template, request, redirect, 
import sqlite3

app = Flask(__name__)

questions = [
    {"text": "When learning something new, I prefer to:", 
     "options": {"A": "See diagrams", "B": "Listen", "C": "Try it", "D": "Read"}},

    {"text": "Before a test I usually:",
     "options": {"A": "Look at summaries", "B": "Explain aloud", "C": "Practice questions", "D": "Re-read notes"}},

    {"text": "I focus best when:", 
     "options": {"A": "Notes look good", "B": "Background sound", "C": "Taking breaks", "D": "Quiet"}},
]

questions = questions * 10   # makes 30 questions


def init_db():
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visual INTEGER,
        auditory INTEGER,
        practical INTEGER,
        reading INTEGER
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html", questions=questions)


def get_recommendation(scores):

    highest = max(scores, key=scores.get)

    if highest == "A":
        return "You learn best visually. Try mind maps, diagrams, colour notes and educational videos."

    elif highest == "B":
        return "You are an auditory learner. Study by explaining topics aloud, discussing with friends, or listening to podcasts."

    elif highest == "C":
        return "You learn best by doing. Use practice questions, experiments, and coding exercises."

    else:
        return "You learn best by reading and writing. Summaries, flashcards, and rewriting notes will work well."


@app.route("/submit", methods=["POST"])
def submit():

    answers = request.form.values()

    scores = {"A": 0, "B": 0, "C": 0, "D": 0}

    for a in answers:
        scores[a] += 1

    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO results (visual, auditory, practical, reading)
    VALUES (?,?,?,?)
    """, (scores["A"], scores["B"], scores["C"], scores["D"]))

    conn.commit()
    conn.close()

    recommendation = get_recommendation(scores)

    return render_template(
        "results.html",
        visual=scores["A"],
        auditory=scores["B"],
        practical=scores["C"],
        reading=scores["D"],
        recommendation=recommendation
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)