
"""Map My Learning."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
#Had to pip install flask_debug_toolbar to get this to run.  
from flask import url_for
from flask_oauth import OAuth
 

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Teacher, TeacherClass, Class, StudentClass, Student, StudentMeasure, Response, Measure, Subject, Objective, Question, QuestionAnswerChoice, AnswerChoice

#This is to access environment variables (GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET) that we loaded via terminal
import os

import json

REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console

# Required to use Flask sessions and the debug toolbar
SECRET_KEY = 'ABC'
DEBUG = True


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

app.jinja_env.undefined = StrictUndefined


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
    
    #Use to view user info returned by Google OAuth
    #print type(user_info_dict)
    #print user_info_dict
    
    #Grabbing email address returned by Google OAuth. Note: Dictionary returned from Google OAuth is called user_info
    #(Changing this to email=user_info.get("email", None) would allow me to set None as the default. 
        #That may be useful when setting up case for creating new accounts) 
    email=user_info_dict["email"]
    #Using email address returned by Google OAuth to query for student_id and storing student_id in web session
    student_object = Student.query.filter_by(username=email).first()
    student_id = student_object.student_id
    student_class_object = StudentClass.query.filter_by(student_id=student_id).first()
    class_id = student_class_object.class_id
    student_class_id = student_class_object.student_class_id

    session["student_id"] = student_id
    session["class_id"] = class_id
    session["student_class_id"] = student_class_id


    return render_template("student-homepage.html")


# @app.route("/map-data.json")
# def map_data():
#     """Return student measure data"""

#     # objectives_objects = Objective.query.all()
#     # print objectives_objects

#     @app.route('/melon-times.json')



@app.route('/objective-averages.json')
def average_objective_self_rating():
    """Returns an average of all self-ratings for each objective."""

    student_id = session["student_id"]
    class_id = session["class_id"]
    objective_list = Objective.query.filter_by(class_id=class_id).all()
    objective_numbers = []
    for objective in objective_list:
        objective_number = objective.objective_number
        objective_numbers.append(objective_number)
    print objective_numbers

    questions_dictionary = {}
    for objective in objective_list:
        questions = Question.query.filter_by(objective_id=objective.objective_id).all()
        print questions

    #session["objective_list"] = objective_list

   
    #TO DO: Make Objective numbers dynamic from list in objective_numbers
    # data_object = Response.query.filter_by(student_id=student_id).all()
    data_dict = {
        "labels": objective_numbers,
        "datasets": [
            {
                "label": "Average Self-Rating",
                "fill": True,
                "lineTension": 0,
                "backgroundColor": "rgba(220,220,220,0.2)",
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
                "data": [2.4, 3.9, 4.8, 4.2, 2.0],
                "spanGaps": False},
            
        ]
    }
    return jsonify(data_dict)



@app.route('/objective-counts.json')
def count_of_objectives():
    """Return data of the count of objective with average self-rating within certain ranges."""

    data_dict = {
                "labels": [
                    "1-2",
                    "3",
                    "4-5"
                ],
                "datasets": [
                    {
                        "data": [12, 4, 6],
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56"
                        ],
                        "hoverBackgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56"
                        ]
                    }]
            }

    return jsonify(data_dict)

    #TO DO: Add a page for students to choose from a list of classes (query StudentClass table for all rows with matching student_id)



@app.route('/end-of-class-survey/<measure_id>', methods=['GET'])
def end_of_class_survey_form(measure_id):
    """Show form for End of Class Survey."""

    #TO DO: Account for case when there is more than one measure in a session
    #Measure id was hard coded in button on homepage that links to this route. This captures the 
    #Measure id and stored it in the session
    session["measure_id"] = measure_id
    #Rebinds the variable name "student"id" to the student_id stored in the session
    student_id = session["student_id"]
    #TO DO: Allow new student measure objects to be created here when I am no
    #long repeatedly answering the same measure
    student_measure_object = StudentMeasure.query.filter_by(student_id=student_id, measure_id=measure_id).first()
    student_measure_id = student_measure_object.student_measure_id
    
    #Queries database for all questions tagged with specified measure_id. Returns a list of objects 
    q_list = Question.query.filter_by(measure_id=measure_id).all()
  
   

    #Renders survey form, passes list of question objects and student measure id to form
    return render_template("end-of-class-survey.html", q_list=q_list, student_measure_id=student_measure_id)
       #TO DO , Send measure _object in above line of code)
        


@app.route('/end-of-class-survey/', methods=['POST'])
def survey_process():
    """Process responses from survey"""

    print request.form

    #Pulls measure_id out of session
    measure_id = session["measure_id"] 
    #This get requests grabs value for student_measure_id that was hidden in the form
    student_measure_id = request.form.get("student_measure_id")
    print student_measure_id
    
    #Names of inputs on survey form are the question id's. Next block of code uses measure id to query database
    #for the list of questions in the form and then creates a list of the question id's used to render survey form
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

    class_id = session["class_id"]
    objective_list = Objective.query.filter_by(class_id=class_id).all()

    
    
  
    
    return render_template("study-notes.html", objective_list=objective_list)


# @app.route('/study_notes/')
# def show_study_notes():
#     """Show personal study notes page"""

#     objective_list = session["objective_list"]
    #TO DO: Account for case when there is more than one measure in a session
    #Measure id was hard coded in button on homepage that links to this route. This captures the 
    #Measure id and stored it in the session
    

    
       #TO DO , Send measure _object in above line of code)


# Need to make separate routes for teacher login and student login

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



# @app.route('/logout')
# def logout():
#     """Log out."""

#     del session["user_id"]
#     flash("Logged Out.")
#     return redirect("/")


# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


# @app.route("/users/<int:user_id>")
# def user_detail(user_id):
#     """Show info about user."""

#     user = User.query.get(user_id)
#     return render_template("user.html", user=user)


# @app.route("/movies")
# def movie_list():
#     """Show list of movies."""

#     movies = Movie.query.order_by('title').all()
#     return render_template("movie_list.html", movies=movies)


# @app.route("/movies/<int:movie_id>", methods=['GET'])
# def movie_detail(movie_id):
#     """Show info about movie.

#     If a user is logged in, let them add/edit a rating.
#     """

#     movie = Movie.query.get(movie_id)

#     user_id = session.get("user_id")

#     if user_id:
#         user_rating = Rating.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

#     return render_template("movie.html",
#                            movie=movie,
#                            user_rating=user_rating)


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables
#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash("Rating updated.")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Rating added.")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
