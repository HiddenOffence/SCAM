from flask import Flask, render_template, request, redirect, url_for, session
from database import (
    create_tables,
    get_sections,
    get_questions_by_section,
    get_answers_by_question,
    calculate_quiz_results,
    get_reviews,
    add_review
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

    # Starting a new quiz clears any previous attempt
    session.pop("quiz_answers", None)

    return render_template("quiz.html")


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

    # To get the current section information
    sections = get_sections()
    current_section = None

    for item in sections:
        if item["id"] == section_id:
            current_section = item
            break

    # Created to temporarily store quiz answers
    if "quiz_answers" not in session:
        session["quiz_answers"] = {}

    # Check whether this question was answered before
    selected_answer = session["quiz_answers"].get(str(current_question["id"]))

    # Runs when the user presses Next or Continue
    if request.method == "POST":
        selected_answer = request.form.get("answer")

        if selected_answer is None:
            return render_template(
                "question.html",
                question=current_question,
                answers=answer_options,
                section=current_section,
                section_id=section_id,
                question_index=question_index,
                total_questions=len(questions),
                selected_answer=selected_answer,
                hide_nav=True)

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
        section=current_section,
        section_id=section_id,
        question_index=question_index,
        total_questions=len(questions),
        selected_answer=selected_answer,
        hide_nav=True)


@app.route("/results")
def results():

    # Get the answers saved while the user completed the quiz
    quiz_answers = session.get("quiz_answers", {})

    # If there are no answers, send the user back to the quiz
    if not quiz_answers:
        return redirect(url_for("quiz"))

    # Get just the answer IDs
    answer_ids = list(quiz_answers.values())

    # Calculate the scores using the database
    quiz_results = calculate_quiz_results(answer_ids)

    # The first result has the highest score
    top_result = quiz_results[0] if quiz_results else None

    return render_template(
        "results.html",
        results=quiz_results,
        top_result=top_result
    )


@app.route("/reviews", methods=["GET", "POST"])
def reviews():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        rating = request.form.get("rating")
        comment = request.form.get("comment", "").strip()

        if name and rating and comment:

            rating = int(rating)

            # Only accept ratings from 1 to 5
            if 1 <= rating <= 5:

                add_review(
                    name,
                    rating,
                    comment
                )

                return redirect(
                    url_for("reviews")
                )

    all_reviews = get_reviews()

    return render_template(
        "reviews.html",
        reviews=all_reviews
    )


if __name__ == "__main__":

    create_tables()

    app.run(debug=True)
