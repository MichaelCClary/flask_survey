from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "jinja"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
question_id = 0


@app.route('/')
def landing_page():
    return render_template("home.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)


@app.route("/questions/<int:id>")
def questions(id):
    if id != question_id:
        flash("Sorry that question wasn't valid, let me fix that for you", 'error')
        return redirect(f"/questions/{question_id}")
    elif id >= len(satisfaction_survey.questions):
        question = "Thank you for your time"
        return render_template("questions.html", question=question)
    else:
        question = satisfaction_survey.questions[id].question
        choices = satisfaction_survey.questions[id].choices
        return render_template("questions.html", question=question, choices=choices)


@app.route("/answer", methods=["POST"])
def answer():
    answer = request.form.get('answer', False)
    if answer:
        responses.append(answer)
        global question_id
        question_id += 1
    else:
        flash("Please answer the question", 'error')
    return redirect(f"/questions/{question_id}")
