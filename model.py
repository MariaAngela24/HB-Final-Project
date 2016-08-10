#Until requirements files is created, need to pip install flask_sqlalchemy and Flask in terminal
"""Models and database functions for Ratings project."""
import heapq
import time
#Delete the line below when server file is created
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#This was from ratings.  Will probably delete if not used
#import correlation


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Teacher(db.Model):
    """Teachers."""

    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Teacher teacher_id=%s username=%s" % (self.teacher_id, self.username)



#double check sty;ing for this type of class and the associated variables
class TeacherClass(db.Model):
    """Association table for teachers and classes."""

    __tablename__ = "teachersClasses"

    teacherClass_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #Double check that the table name should be plural
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    #Variable below is not in MVP
    permission_level = db.Column(db.String(25), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<TeacherClass teacherClass_id=%s teacher_id=%s class_id=%s" % (self.teacherClass_id, self.teacher_id, self.class_id)



class Class(db.Model):
    """Classes."""

    __tablename__ = "classes"

    class_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'))
       

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Class class_id=%s subject_id=%s>" % (self.class_id, self.subject_id)



class StudentClass(db.Model):
    """Association table for teachers and classes."""

    __tablename__ = "studentsClasses"

    studentClass_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<StudentClass studentClass_id=%s student_id=%s class_id=%s" % (self.studentClass_id, self.student_id, self.class_id)



class Student(db.Model):
    """Enrolled students."""

    __tablename__ = "students"

    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #What are the tradeoffs for setitng some of these to 'False' for nullable?
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    grade = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    #If I plan to use the Google API, does this change?
    username = db.Column(db.String(64), nullable=True)
    #How can I set upper and lower bounds for a password?
    password = db.Column(db.String(64), nullable=True)
    #Need to verify that the data we have for math and reading levels is quantitative
    math_level = db.Column(db.Integer, nullable=True)
    reading_level = db.Column(db.Integer, nullable=True)

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Student student_id=%s username=%s" % (self.student_id, self.username)



class StudentMeasure(db.Model):
    """Association table for students and measures."""

    __tablename__ = "studentsMeasures"

    studentMeasure_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    measure_id = db.Column(db.Integer, db.ForeignKey('measures.measure_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<StudentMeasure studentMeasure_id=%s measure_id=%s student_id=%s" % (self.studentMeasure_id, self.measure_id, self.student_id)



class Response(db.Model):
    """Association table for students and measures."""

    __tablename__ = "responses"

    response_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    studentMeasure_id = db.Column(db.Integer, db.ForeignKey('studentsMeasures.studentMeasure_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    #Is this a good character limit for a text field?
    response = db.Column(db.String(500), nullable=True)


def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Response reasponse_id=%s studentMeasure_id=%s response=%s" % (self.response_id, self.studentMeasure_id, self.response_id, self.student_id)



class Measure(db.Model):
    """Measures such as homework surveys, end of class surveys, and quizzes"""

    __tablename__ = "measures"

    measure_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    #The variable below indicates the type of measure, such as homework survey
    #end of class survey, or quiz
    flag = db.Column(db.String(64), nullable=True)
    #This is a timestamp for when the measure was administered.  Do I need when it closed
    #as a variable in this database or do I control for it on the flask side?
    #sent_time = db.Column(db Datetime????) 
    #The variable below tracks whether measure has never been opened, is open and waiting
    #for responses, or is closed
    status = flag = db.Column(db.String(20), nullable=True)
       

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Measure measure_id=%s class_id=%s sent_time=%s>" % (self.measure_id, self.class_id, self.sent_time)



class Subject(db.Model):
    """Subjects (examples: Statisitics, Algebra, Geometry)."""

    __tablename__ = "subjects"

    subject_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    course_number = db.Column(db.String(25), nullable=True)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Subject subject_id=%s name=%s" % (self.subject_id, self.name)

class Objective(db.Model):
    """Learning objectives"""

    __tablename__ = "objectives"

    objective_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Objective objective_id=%s name=%s" % (self.objective_id, self.name)



class Question(db.Model):
    """Questions."""

    __tablename__ = "questions"

    question_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    measure_id = db.Column(db.Integer, db.ForeignKey('measures.measure_id'))
    objective_id = db.Column(db.Integer, db.ForeignKey('objectives.objective_id'))
    prompt = db.Column(db.String(500), nullable=False)
    #this is used to indicate questions that are part of the standard set for 
    #certain measures
    flag = db.Column(db.String(25), nullable=True)
    #this indicates multiple choice, free response, etc
    question_type = db.Column(db.String(25), nullable=True)
    correct_answer = db.Column(db.Integer, db.ForeignKey('answersChoices.answerC.crehoice_id'))


def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Question question_id=%s prompt=%s flag=%s" % (self.question_id, self.prompt, self.flag)



class QuestionAnswerChoice(db.Model):
    """Association table between questions and Answer Choices. Used for multiple choice questions"""

    __tablename__ = "questionAnswerChoices"

    questionAnswerChoice_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    answerChoice_id = db.Column(db.Integer, db.ForeignKey('answersChoices.answerChoice_id'))
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<AnswerChoice answer_choice_id=%s question_id=%s answerChoice_id=%s" % (self.questionAnswerChoice_id, self.question_id, self.answerChoice_id)



class AnswerChoice(db.Model):
    """Answer Choices."""

    __tablename__ = "answersChoices"

    answerChoice_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #What should I do for other answer choice types, such as images?
    text = db.Column(db.String(150), nullable=True)
    #Do I need to make any additional specifications?
    Value = db.Column(db.Integer, nullable=True)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<AnswerChoice answerChoice_id=%s text=%s value=%s" % (self.answerChoice_id, self.text, self.value)


# class Rating(db.Model):
#     """Rating of a movie by a user."""

#     __tablename__ = "ratings"
 
#     rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     score = db.Column(db.Integer)

#     # Define relationship to user
#     user = db.relationship("User",
#                            backref=db.backref("ratings", order_by=rating_id))

#     # Define relationship to movie
#     movie = db.relationship("Movie",
#                             backref=db.backref("ratings", order_by=rating_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
#             self.rating_id, self.movie_id, self.user_id, self.score)


##############################################################################
# Helper functions
#move this line back to server file when that is created
app = Flask(__name__)
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///system'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    #Uncomment when line 191 is moved back to server
    #from server import app
    connect_to_db(app)
    print "Connected to DB."
