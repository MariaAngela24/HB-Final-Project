#Until requirements files is created, need to pip install flask_sqlalchemy and Flask in terminal
"""Models and database functions for Ratings project."""
import heapq
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of the interactions (like committing, etc.)

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
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Teacher teacher_id=%s username=%s" % (self.teacher_id, self.username)



class TeacherClass(db.Model):
    """Association table for teachers and classes."""

    __tablename__ = "teachers_classes"

    teacher_class_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    #Variable below is not in MVP
    permission_level = db.Column(db.String(25), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<TeacherClass teacher_class_id=%s teacher_id=%s class_id=%s" % (self.teacher_class_id, self.teacher_id, self.class_id)



class Class(db.Model):
    """Classes."""

    __tablename__ = "classes"

    class_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'))
    name = db.Column(db.String(64), nullable=True)
    #TO DO: Need to find a way to account for term in the data model

    teachers = db.relationship("Teacher", 
                            secondary="teachers_classes",
                            backref=db.backref("classes"))


       

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Class class_id=%s subject_id=%s>" % (self.class_id, self.subject_id)



class StudentClass(db.Model):
    """Association table for students and classes."""

    __tablename__ = "students_classes"

    student_class_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<StudentClass student_class_id=%s student_id=%s class_id=%s" % (self.student_class_id, self.student_id, self.class_id)



class Student(db.Model):
    """Enrolled students."""

    __tablename__ = "students"

    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    grade = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(64), nullable=True)
    math_placement = db.Column(db.String(25), nullable=True)
    reading_grade_equivalent = db.Column(db.Float, nullable=True)

    classes = db.relationship("Class", 
                            secondary="students_classes",
                            backref=db.backref("students", order_by=last_name))

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Student student_id=%s username=%s" % (self.student_id, self.username)



class StudentMeasure(db.Model):
    """Association table for students and measures."""

    __tablename__ = "students_measures"

    student_measure_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    measure_id = db.Column(db.Integer, db.ForeignKey('measures.measure_id'))
    
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<StudentMeasure student_measure_id=%s measure_id=%s student_id=%s" % (self.student_measure_id, self.measure_id, self.student_id)



class Response(db.Model):
    """Responses to measures."""

    __tablename__ = "responses"

    response_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_measure_id = db.Column(db.Integer, db.ForeignKey('students_measures.student_measure_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    response = db.Column(db.String(500), nullable=True)

    # TO DO: decide if I need to define relationship to any other tables


    def __repr__(self):
            """Provide helpful representation when printed."""

            return "<Response response_id=%s student_measure_id=%s response=%s" % (self.response_id, self.student_measure_id, self.response)



class Measure(db.Model):
    """Measures such as homework surveys, end of class surveys, and quizzes"""

    __tablename__ = "measures"

    measure_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    #The variable below indicates the type of measure, such as homework survey
    #end of class survey, or quiz
    flag = db.Column(db.String(64), nullable=True)  
    #TO DO: Add datetime variable
    #sent_time = db.Column(db Datetime????) 
    #The variable below tracks whether measure has never been opened, is open and waiting
    #for responses, or is closed
    status = db.Column(db.String(20), nullable=True)

    students = db.relationship("Student", 
                            secondary="students_measures", order_by=Student.last_name,
                            backref=db.backref("measures"))
       

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Measure measure_id=%s class_id=%s>" % (self.measure_id, self.class_id)



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



#TO DO: Need to account for many to many relationship between objectives and questions. 
#Also need to account for many to many relationship between objectives and classes
class Objective(db.Model):
    """Learning objectives"""

    __tablename__ = "objectives"

    objective_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    objective_number = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))



    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Objective objective_id=%s name=%s" % (self.objective_id, self.name)



class AnswerChoice(db.Model):
    """Answer Choices."""

    __tablename__ = "answers_choices"

    answer_choice_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.String(150), nullable=True)
    value = db.Column(db.Float, nullable=True)
    position = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<AnswerChoice answerChoice_id=%s text=%s value=%s" % (self.answer_choice_id, self.text, self.value)



class Question(db.Model):
    """Questions."""

    __tablename__ = "questions"

    question_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    measure_id = db.Column(db.Integer, db.ForeignKey('measures.measure_id'))
    objective_id = db.Column(db.Integer, db.ForeignKey('objectives.objective_id'))
    prompt = db.Column(db.String(500), nullable=False)
    #This variable is used to indicate questions that are part of the standard set for 
    #certain measures
    measure_type = db.Column(db.String(50), nullable=True)
    #This variable indicates multiple choice, free response, etc
    question_type = db.Column(db.String(50), nullable=True)
    #This variable indicates whether it is a reading, homework, groupwork, lecture notes, or overall understanding question
    question_content = db.Column(db.String(50), nullable=True)
    position = db.Column(db.Integer, nullable=True)

    #Add the column below when quizzes are added to the data
    #correct_answer = db.Column(db.Integer, db.ForeignKey('answers_choices.answer_choice_id'), nullable=True)


    answer_choices = db.relationship("AnswerChoice", 
                            secondary="questions_answer_choices", order_by=AnswerChoice.answer_choice_id,
                            backref=db.backref("questions"))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Question question_id=%s question_type=%s" % (self.question_id, self.question_type)




def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Question question_id=%s prompt=%s flag=%s" % (self.question_id, self.prompt, self.flag)





class QuestionAnswerChoice(db.Model):
    """Association table between questions and Answer Choices. Used for multiple choice questions"""

    __tablename__ = "questions_answer_choices"

    question_answer_choice_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    answer_choice_id = db.Column(db.Integer, db.ForeignKey('answers_choices.answer_choice_id'))
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<AnswerChoice answer_choice_id=%s question_id=%s answerChoice_id=%s" % (self.question_answer_choice_id, self.question_id, self.answer_choice_id)






##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///system'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)



def example_data():
    """Create some sample data."""

    subject = Subject(name='Subject 1')
    db.session.add(subject)
    db.session.commit()

    objective = Objective(name='Regression')
    student = Student(username='johnsmith')
    class_row = Class(subject_id=1)
    db.session.add_all([objective, student, class_row])
    db.session.commit()

    measure = Measure(class_id=1)
    db.session.add(measure)
    db.session.commit()

    student_measure = StudentMeasure(student_id=1, measure_id=1)
    db.session.add(student_measure)
    db.session.commit

    q1 = Question(measure_id=1, objective_id=1, prompt="Question 1")
    q2 = Question(measure_id=1, objective_id=1, prompt="Question 2")
    q3 = Question(measure_id=1, objective_id=1, prompt="Question 3")
    db.session.add_all([q1, q2, q3])
    db.session.commit()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."
