from flask import Flask, render_template
from database import create_tables, populate_study_methods


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


if __name__ == "__main__":

    create_tables()
    populate_study_methods()

    app.run(debug=True)
