
"""Map My Learning."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
#I had to pip install flask_debug_toolbar to get this to run.  Do I need to do anything to get that
#to work in the future?
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Teacher, TeacherClass, Class, StudentClass, Student, StudentMeasure, Response, Measure, Subject, Objective, Question, QuestionAnswerChoice, AnswerChoice


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Student Homepage."""

    #TO DO: Need to add if/else that redirects students who are not logged into
    #the login page and students who are logged in to their homepage

    #TO DO: Jinja needs to be added in the else statement to enable student to see
    #their personal data

    return render_template("student-homepage.html")


@app.route('/end-of-class-survey', methods=['GET'])
def end_of_class_survey_form():
    """Show form for End of Class Survey."""

    #TO DO: Once teacher forms are built, the measure_id determines which survey
    #to render. Be sure to comment out measure_id hard coding


    return render_template("end-of-class-survey.html", measure_id=measure_id)


@app.route('/end-of-class-survey/<int:measure_id>', methods=['POST'])
def register_process(measure_id):
    """Process registration."""

    # Get form variables
    lecture_notes_rating = request.form.get("lecture-and-notes")
    key_words = request.form.get("key-words")
    group_problems_rating = request.form.get("group-problems")
    problems_to_revisit = request.form.get("problems-to-revisit")
    overall_rating = request.form.get("overall")
    questions = request.form.get("questions")
    

    #QUESTION & TO DO: Each new response and each new question should be unique id's.  How do I code this as a variable?
    response_1  = Response(response=lecture_notes_rating, student_measure_id=students_measures.student_measure_id, question_id=1)
    response_2  = Response(response=key_words, student_measure_id=students_measures.student_measure_id, question_id=2)
    response_3  = Response(response=group_problems_rating, student_measure_id=students_measures.student_measure_id, question_id=3)
    response_4  = Response(response=problems-to-revisit, student_measure_id=students_measures.student_measure_id, question_id=4)
    response_5  = Response(response=overall_rating, student_measure_id=students_measures.student_measure_id, question_id=5)
    response_6  = Response(response=questions, student_measure_id=students_measures.student_measure_id, question_id=6)

    #TO DO: Change this to a loop 
    db.session.add(response_1)
    db.session.add(response_2)
    db.session.add(response_3)
    db.session.add(response_4)
    db.session.add(response_5)
    db.session.add(response_6)


    db.session.commit()

    return render_template("survey-acknowledgement.html")

# Need to make separate routes for teacher login and student login

# @app.route('/student-login', methods=['GET'])
# def student_login_form():
#     """Show login form."""

#     return render_template("student_login_form.html")


# @app.route('/student-login', methods=['POST'])
# def student_login_process():
#     """Process login."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]

      #Need to change email to whatever is required/available in GoogleAuth     
#     student = Student.query.filter_by(email=email).first()

#     if not user:
#         flash("No such user")
#         return redirect("/login")

#     session["student_id"] = student.student_id

#     flash("Logged in")
#     return redirect("/")


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
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
