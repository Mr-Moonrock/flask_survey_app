from surveys import satisfaction_survey as survey
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension


RESPONSES_KEY = "responses"

#key names will use to store some things in the session;
#put here as constants so we're guaranteed to be consistent in our spelling of these

app = Flask(__name__)
app.secret_key = "mrMoonrock"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

@app.route('/')
def home_page():
    """Select as survey"""
    return render_template('survey_start.html', survey=survey)

@app.route("/begin", methods=['POST'])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/answers', methods=['POST'])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']
    # add this response to the session
    responses= session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        #They've answered all the questions! Thank them.
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect('/complete')
    
    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect('complete')
    
    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template(
        "survey_questions.html", question_num=qid, question=question)


@app.route('/complete')
def complete(): 

    return render_template("completion.html") 

if __name__ == "__main__":
    app.run(debug=True)

