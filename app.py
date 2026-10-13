'''SCAM Don't CRAM 2026'''
from flask import Flask, render_template, request, redirect, url_for, session
from database import (
    create_tables,
    get_sections,
    get_questions_by_section,
    get_answers_by_question,
    calculate_quiz_results,
    get_reviews,
    add_review,
    get_valid_quiz_answers
)
from forms import ReviewForm


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

    # Prevent invalid section IDs from reaching the template.
    if section is None or not questions:
        return render_template("404.html", hide_nav=True), 404

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

    # Process the answer when Next or Continue is clicked.
    if request.method == "POST":
        submitted_answer = request.form.get("answer")

        # Reject missing or non-numeric answer IDs.
        try:
            answer_id = int(submitted_answer)
        except (TypeError, ValueError):
            return "Please select a valid answer.", 400

        # Only accept answers belonging to this question.
        valid_answer_ids = {
            answer["id"] for answer in answer_options
        }

        if answer_id not in valid_answer_ids:
            return "Invalid answer for this question.", 400

        # Save the validated answer for this quiz attempt.
        quiz_answers = session["quiz_answers"]
        quiz_answers[str(current_question["id"])] = answer_id
        session["quiz_answers"] = quiz_answers

        # Continue to the next question in this section.
        if question_index + 1 < len(questions):
            return redirect(
                url_for(
                    "question",
                    section_id=section_id,
                    question_index=question_index + 1
                )
            )

        # After question five, introduce the next section.
        sections = get_sections()
        section_ids = [item["id"] for item in sections]

        current_position = section_ids.index(section_id)

        if current_position + 1 < len(section_ids):
            return redirect(
                url_for(
                    "quiz_section",
                    section_id=section_ids[current_position + 1]
                )
            )

        # The last section leads to the results page.
        return redirect(url_for("results"))

    # Display the question page for GET requests.
    return render_template(
        "question.html",
        question=current_question,
        answers=answer_options,
        section=current_section,
        section_id=section_id,
        question_index=question_index,
        total_questions=len(questions),
        selected_answer=selected_answer,
        hide_nav=True
    )


@app.route("/results")
def results():
    """Calculate recommendations from validated quiz answers."""

    # Retrieve answers stored during the current attempt.
    quiz_answers = session.get("quiz_answers", {})

    if not isinstance(quiz_answers, dict) or not quiz_answers:
        return redirect(url_for("quiz"))

    # Retrieve valid question-answer relationships from SQLite.
    valid_answers = get_valid_quiz_answers()

    # Require one answer for every question in the database.
    if len(quiz_answers) != len(valid_answers):
        return redirect(url_for("quiz"))

    answer_ids = []

    for question_id, selected_answer in quiz_answers.items():

        # Reject invalid question IDs or answer values.
        try:
            question_id = int(question_id)
            answer_id = int(selected_answer)
        except (TypeError, ValueError, OverflowError):
            return redirect(url_for("quiz"))

        # Confirm the answer belongs to the correct question.
        if (
            question_id not in valid_answers
            or answer_id not in valid_answers[question_id]
        ):
            return redirect(url_for("quiz"))

        answer_ids.append(answer_id)

    # Score only answers that passed server-side validation.
    quiz_results = calculate_quiz_results(answer_ids)

    # Identify all strategies tied for the highest score.
    top_results = []

    if quiz_results:
        highest_score = quiz_results[0]["score"]

        top_results = [
            result
            for result in quiz_results
            if result["score"] == highest_score
        ]

    return render_template(
        "results.html",
        results=quiz_results,
        top_results=top_results
    )


@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    """Display student reviews and validate new submissions."""

    # Create the form, including its CSRF token.
    form = ReviewForm()

    if form.validate_on_submit():

        name = form.name.data.strip()
        comment = form.comment.data.strip()

        # Convert the validated rating safely to an integer.
        try:
            rating = int(form.rating.data)
        except (TypeError, ValueError):
            form.rating.errors.append(
                "Please select a valid rating."
            )
        else:
            # Validate values again after removing whitespace.
            if not name:
                form.name.errors.append(
                    "Please enter your name."
                )
            elif not comment:
                form.comment.errors.append(
                    "Please enter your review."
                )
            elif not 1 <= rating <= 5:
                form.rating.errors.append(
                    "Rating must be between 1 and 5."
                )
            else:
                # Store only validated reviews in SQLite.
                add_review(name, rating, comment)

                return redirect(url_for("reviews"))

    # Retrieve existing reviews for both GET and invalid POST.
    all_reviews = get_reviews()

    return render_template(
        "reviews.html",
        reviews=all_reviews,
        form=form,
    )


@app.errorhandler(404)
def page_not_found(error):
    """Display a custom 404 page without the navigation bar."""

    return render_template(
        "404.html",
        hide_nav=True
    ), 404


if __name__ == "__main__":

    create_tables()

    app.run(debug=True)
