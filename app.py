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

    # Getting the 5 questions that belong to this section
    questions = get_questions_by_section(section_id)

    # Stops from creating invalid question numbers
    if question_index < 0 or question_index >= len(questions):
        return "Question not found", 404

    # Getting the current question
    current_question = questions[question_index]

    # Getting the 4 answers for this question
    answer_options = get_answers_by_question(
        current_question["id"]
    )

    # Created to temporarily store quiz answers
    if "quiz_answers" not in session:
        session["quiz_answers"] = {}

    # Runs when the user presses Next or Continue
    if request.method == "POST":
        selected_answer = request.form.get("answer")

        if selected_answer is None:
            return render_template(
                "question.html",
                question=current_question,
                answers=answer_options,
                section_id=section_id,
                question_index=question_index,
                total_questions=len(questions)
            )
        # Saves this answer in the session
        quiz_answers = session["quiz_answers"]

        quiz_answers[
            str(current_question["id"])
        ] = int(selected_answer)

        session["quiz_answers"] = quiz_answers
        # Questions 1-4:
        # Moving to the next question
        if question_index + 1 < len(questions):
            return redirect(
                url_for(
                    "question",
                    section_id=section_id,
                    question_index=question_index + 1
                )
            )
        # Question 5 in Sections 1-5:
        # Shows the NEXT section introduction card
        if section_id < 6:

            return redirect(
                url_for(
                    "quiz_section",
                    section_id=section_id + 1
                )
            )
        # Quiz finishes
        return redirect(
            url_for("results")
        )

    return render_template(
        "question.html",
        question=current_question,
        answers=answer_options,
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
