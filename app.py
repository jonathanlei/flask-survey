from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys as surveys_dict

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def generate_survey_selections():
    """ generate a dropdown menu of survery selections"""
    return render_template(
        "surveys_selection.html",
        surveys_dict=surveys_dict
    )


@app.route("/start", methods=["POST"])
def generate_survey_start_page():
    """ generate a homepage with title, instruction and start button of a survey selected"""
    survey_name = request.form["survey_name"]
    survey = surveys_dict[survey_name]
    #saving current survey name
    # session["survey_name"] = survey_name
    
    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions,
        survey_name=survey_name)


@app.route("/<survey_name>/begin", methods=["POST"])
def start_survey(survey_name):
    """ redirecting to question page, and reset responses list"""
    # have the key name be the survey name 
    session[survey_name] = []
    return redirect(f"/{survey_name}/questions/0")


@app.route("/<survey_name>/questions/<int:number>")
def generate_question(survey_name, number):
    """ generate a question page from the question list based on the number """
    # check if the number from the url is the correct question the user should 
    # be answering
    current_response_num = len(session[survey_name])
    if number != current_response_num:
        flash(f"Invalid number {number} in survey")
        return redirect(f"/{survey_name}/questions/{current_response_num}")
    
    # #getting the current survey 
    # survey_name = session["survey_name"]
    # survey = surveys_dict[survey_name]
    survey = surveys_dict[survey_name]
    question = survey.questions[number]
    return render_template(
        "question.html",
        question=question,
        number=number,
        survey_name=survey_name)


@app.route("/<survey_name>/answer/<int:number>", methods=["POST"])
def store_answer(survey_name, number):
    """ store the answer and redirect to next question page"""
    responses = session[survey_name]
    responses.append(
        {"answer": request.form["answer"],
        "text_answer": request.form.get("text_answer")})
    session[survey_name] = responses
    
    print(session[survey_name], "session responses")

    # #getting the current survey 
    # survey_name = session["survey_name"]
    # survey = surveys_dict[survey_name]
    survey = surveys_dict[survey_name]
    redirect_url = (
        f"/{survey_name}/questions/{number+1}"
        if len(responses) < len(survey.questions)
        else "/thanks")
    return redirect(redirect_url)


@app.route("/thanks")
def generate_thanks():
    """ show the thank you page"""
    return render_template("completion.html")
