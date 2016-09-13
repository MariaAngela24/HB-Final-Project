
"""Map My Learning."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify  
from flask import url_for
from flask_oauth import OAuth
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Teacher, TeacherClass, Class, StudentClass, Student, StudentMeasure, Response, Measure, Subject, Objective, Question, QuestionAnswerChoice, AnswerChoice
from sqlalchemy.sql import func
from sqlalchemy import cast, Numeric

#This is to access environment variables (GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET) that we loaded via terminal
import os
import json

# one of the Redirect URIs from Google APIs console
REDIRECT_URI = '/oauth2callback'  
# Required to use Flask sessions and the debug toolbar
SECRET_KEY = 'ABC'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
app.jinja_env.undefined = StrictUndefined

oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=os.environ["GOOGLE_CLIENT_ID"],
                          consumer_secret=os.environ["GOOGLE_CLIENT_SECRET"]
)



@app.route('/')
def index():
    """Show Student Homepage."""

    #Next 5 blocks of code are for Google OAuth 
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError
 
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)

    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
 
    user_info = res.read()
    user_info_dict = json.loads(user_info)
    
    #Use next two linesto view user info returned by Google OAuth
    #print type(user_info_dict)
    #print user_info_dict
    
    #Grabbing email address returned by Google OAuth. Note: Dictionary returned from Google OAuth is called user_info
    #Note: Changing this to email=user_info.get("email", None) would allow me to set None as the default. 
    #That may be useful when setting up case for creating new accounts. 
    email=user_info_dict["email"]
    #Using email address returned by Google OAuth to query for student object 
    student_object = Student.query.filter_by(username=email).first()
    #getting student_id and username from student_object 
    student_id = student_object.student_id
    username = student_object.username
    #Using student_id to query database for student_class object
    #TO DO: Need to account for case when students are in multiple classes
    student_class_object = StudentClass.query.filter_by(student_id=student_id).first()
    #getting class_id and student_class_id from student_class object
    class_id = student_class_object.class_id
    student_class_id = student_class_object.student_class_id

    #storing id's and username in web session to be able to access them in other routes
    session["student_id"] = student_id
    session["class_id"] = class_id
    session["student_class_id"] = student_class_id
    session["username"] = username


    return render_template("student-homepage.html")



@app.route('/objective-averages.json')
def average_objective_self_rating():
    """Returns an average of all self-ratings for each objective."""

    #Rebind student_id and class_id to values in session
    student_id = session["student_id"]
    class_id = session["class_id"]
    #Get list of all objective objects
    objective_list = Objective.query.filter_by(class_id=class_id).all()
    #Create lists of just objective numbers and objective_ids from objective object
    objective_numbers = []
    for objective in objective_list:
        objective_number = objective.objective_number
        objective_numbers.append(objective_number)

    objective_ids = []
    for objective in objective_list:
        objective_id = objective.objective_id
        objective_ids.append(objective_id)


    #Create a list of tuples that contains objective_id and response for all questions answered by student
    #Need to look up what numeric means and see if adjusting that will get me a value with less decimal places
    #Need to convert average value from a decimal back to something JSON serializable, which is probably going to 
    #be a string.  Easiest answer may be to cast it back to a string. Need to look at available types for JSON
    response_tuples = db.session.query(Question.objective_id, func.avg(cast(Response.response, Numeric(10, 4)))).\
                                        filter(Question.question_type=="Likert scale", StudentMeasure.student_id==student_id).\
                                        join(Response).\
                                        join(StudentMeasure).\
                                        group_by(Question.objective_id).\
                                        all()
    print "response_tuples=", response_tuples
    
    #Create dictionary of objective_ids and responses
    response_dictionary = dict(response_tuples)
    print "response_dictionary=", response_dictionary

    #Creating a list of responses in order by objective_id
    response_data = []
    for item in objective_ids:
        response_value = response_dictionary.get(item)
        response_data.append(response_value)
   
    
    #Creating a dictionary of data and chart options that can be sent to student homepage
    data_dict = {
        "labels": objective_numbers,
        "datasets": [
            {
                "label": "Average self-rating by learning objective",
                "fill": True,
                "lineTension": 0,
                "backgroundColor": "rgba(220,220,220,0.6)",
                "borderColor": "rgba(220,220,220,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(220,220,220,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": response_data,
                "spanGaps": False},
            
        ]
    }

    #jsonify command is necessary because data above must be passed through route as a string
    return jsonify(data_dict)



@app.route('/objective-counts.json')
def count_of_objectives():
    """Return data of the count of objective with average self-rating within certain ranges."""

    #Creating donut chart
    data_dict = {
                "labels": [
                    "Objectives I understand well",
                    "Objectives I partially understand",
                    "Objectives I do not understand"
                ],
                "datasets": [
                    {
                        "data": [12, 4, 6],
                        "backgroundColor": [
                            "#4CAF50",
                            "#FFC107",
                            "#F44336"
                        ],
                        "hoverBackgroundColor": [
                            "#4CAF50",
                            "#FFC107",
                            "#F44336"
                            
                        ]
                    }]
            }

    return jsonify(data_dict)



@app.route('/end-of-class-survey/<measure_id>', methods=['GET'])
def end_of_class_survey_form(measure_id):
    """Show form for End of Class Survey."""



    #Captures measure_id sent to route when student clicks survey button on homepage
    #TO DO: Account for case when there is more than one measure in a session
    session["measure_id"] = measure_id
    #Uses measure_id to query database for measure object
    measure_object = Measure.query.filter_by(measure_id=measure_id).first()
    #Rebinds the variable name "student"id" to the student_id stored in the session
    student_id = session["student_id"]
    #TO DO: Add functionality that allows new student measure objects to be created
    student_measure_object = StudentMeasure.query.filter_by(student_id=student_id, measure_id=measure_id).first() 
    student_measure_id = student_measure_object.student_measure_id
    
    #Queries database for all questions tagged with specified measure_id. Returns a list of objects 
    q_list = Question.query.filter_by(measure_id=measure_id).all()
  

    #Renders survey form, passes list of question objects and student measure id to form
    return render_template("end-of-class-survey.html", q_list=q_list, student_measure_id=student_measure_id, measure_object=measure_object)
       #TO DO , Send measure _object in above line of code)
        


@app.route('/end-of-class-survey/', methods=['POST'])
def survey_process():
    """Process responses from survey"""


    #Pulls measure_id out of session
    measure_id = session["measure_id"] 
    #Grabs value for student_measure_id that was hidden in the form
    student_measure_id = request.form.get("student_measure_id")
    
    #Names of inputs on survey form are the question id's, so question_ids are variables. Next block of code uses measure id to query database
    #for the question objects that rendered on the form, then creates a new list of the question id's used to render the survey form
    q_list = Question.query.filter_by(measure_id=measure_id).all()
    question_ids = []
    for question in q_list:
        question_id = question.question_id
        question_ids.append(question_id)
    
    i = 0
    for item in question_ids:
        #For each item in q_list, bind the name question_id to the value of the item
        question_id = question_ids[i]
        #str() function is used inside get request because question_id's that are used as names on form are stored as strings 
        response_text_or_value = request.form.get(str(question_id))
        #Create a new response row and add it to the database
        response_row = Response(response=response_text_or_value, student_measure_id=student_measure_id, question_id=question_id)
        db.session.add(response_row)
        i = i + 1
        
    db.session.commit()  
  
    return render_template("survey-acknowledgement.html")



@app.route('/study-notes/')
def show_study_notes():
    """Show personal study notes page"""

    #TO DO: Complete this feature
    class_id = session["class_id"]
    objective_list = Objective.query.filter_by(class_id=class_id).all()
  
    
    return render_template("study-notes.html", objective_list=objective_list)



#TO DO: make separate routes for teacher login and student login

@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

    #_external=True



@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))



@google.tokengetter
def get_access_token():
    return session.get('access_token')



#TO DO: Add logout functionality
# @app.route('/logout')
# def logout():
#     """Log out."""

#     del session["user_id"]
#     flash("Logged Out.")
#     return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
