from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def generate_homepage():
    """ generate a homepage with title, instruction and start button of a survey"""
    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions)


@app.route("/begin", methods=["POST"])
def start_survey():
    """ redirecting to question page, and reset responses list"""
    responses.clear()
    return redirect("/questions/0")


@app.route("/questions/<int:number>")
def generate_question(number):
    """ generate a question page from the question list based on the number"""
    question = survey.questions[number]
    return render_template(
        "question.html",
        question=question,
        number=number)


@app.route("/answer/<int:number>", methods=["POST"])
def store_answer(number):
    """ store the answer and redirect to next question page"""
    responses.append(request.form["answer"])
    redirect_url = (
        f"/questions/{number+1}"
        if len(responses) < len(survey.questions)
        else "/thanks")
    return redirect(redirect_url)


@app.route("/thanks")
def generate_thanks():
    """ show the thank you page"""
    print(responses, survey.questions)
    return render_template("completion.html")
