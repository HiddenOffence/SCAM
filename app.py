from flask import Flask, render_template, request, redirect, url_for, session
from database import (
    create_tables,
    get_sections,
    get_questions_by_section,
    get_answers_by_question
)


app = Flask(__name__)
app.secret_key = "scam_your_study2026"


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


@app.route(
    "/quiz/<int:section_id>/question/<int:question_index>",
    methods=["GET", "POST"])
def question(section_id, question_index):

    questions = get_questions_by_section(section_id)

    if question_index < 0 or question_index >= len(questions):
        return "Question not found", 404

    current_question = questions[question_index]

    answers = get_answers_by_question(current_question["id"])
    if request.method == "POST":
        selected_answer = request.form.get("answer")
        if selected_answer:
            if "answers" not in session:
                session["answers"] = {}
            answers_dict = session["answers"]
            answers_dict[str(current_question["id"])] = selected_answer
            session["answers"] = answers_dict

            if question_index + 1 < len(questions):
                return redirect(
                    url_for(
                        "question",
                        section_id=section_id,
                        question_index=question_index + 1
                    )
                )
            else:
                return redirect(url_for("results"))

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
