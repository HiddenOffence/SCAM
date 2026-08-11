from flask import Flask, render_template
from database import (
    create_tables,
    get_sections,
    get_questions_by_section,
    get_answers_by_question
)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/quiz")
def quiz():
    sections = get_sections()
    return render_template("quiz.html", sections=sections)


@app.route("/quiz/<int:section_id>")
def quiz_section(section_id):

    sections = get_sections()

    questions = get_questions_by_section(section_id)

    section = None

    for item in sections:
        if item["id"] == section_id:
            section = item
            break

    return render_template(
        "quiz_section.html",
        section=section,
        questions=questions,
        section_id=section_id
    )


@app.route("/quiz/<int:section_id>/question/<int:question_index>")
def question(section_id, question_index):

    questions = get_questions_by_section(section_id)

    if question_index < 0 or question_index >= len(questions):
        return "Question not found", 404

    current_question = questions[question_index]

    answers = get_answers_by_question(current_question["id"])

    return render_template(
        "question.html",
        question=current_question,
        answers=answers,
        section_id=section_id,
        question_index=question_index,
        total_questions=len(questions)
    )


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


if __name__ == "__main__":

    create_tables()

    app.run(debug=True)
