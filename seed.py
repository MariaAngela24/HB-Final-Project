"""Utility file to seed system database from sample data in seed_data/"""

import datetime
from sqlalchemy import func

from model import Teacher, TeacherClass, Class, StudentClass, Student, StudentMeasure, Response, Measure, Subject, Objective, Question, QuestionAnswerChoice, AnswerChoice, connect_to_db, db 


from server import app

def load_teachers():
    """Load a single teacher into database."""

    print "Teachers"

    teacher = Teacher(first_name="Maria", 
                    last_name="Mendiburo", 
                    username="username", 
                    password="password")
    db.session.add(teacher)
    db.session.commit()



def load_subjects():
    """Load two subjects into database from u.subject"""

    print "Subjects"

    for i, row in enumerate(open("seed_data/u.subject.txt")):
        row = row.rstrip()
        name, description, course_number = row.split("|")
        subject = Subject(name=name, 
                        description=description, 
                        course_number=course_number) 
                        
        db.session.add(subject)

    db.session.commit()



def load_classes():
    """Load three classes into database from u.class."""

    print "Classes"

    for i, row in enumerate(open("seed_data/u.class.txt")):
        row = row.rstrip()
        subject_id, name = row.split("|")
        _class = Class(subject_id=subject_id, 
                    name=name) 
                        
        db.session.add(_class)

    db.session.commit()




def load_students():
    """Load students from u.student into database."""

    print "Students"

    for i, row in enumerate(open("seed_data/u.student.txt")):
        row = row.rstrip()
        first_name, last_name, grade, gender, username, password, math_level, math_placement, reading_grade_equivalent = row.split("|")
        student = Student(
                        first_name=first_name, 
                        last_name=last_name, 
                        grade=grade, 
                        gender=gender, 
                        username=username, 
                        password=password, 
                        math_placement=math_placement, 
                        reading_grade_equivalent=reading_grade_equivalent)

        db.session.add(student)

    db.session.commit()


#TO DO: Change this to three measures so there is one for each class
def load_measures():
    """Load a single measure into database."""

    print "Measures"

    measure = Measure(class_id=1, 
                    flag="end class survey", 
                    #To Do: uncomment after fixing datetime in model.py sent_time=???
                    status="never opened")
    db.session.add(measure)
    db.session.commit()



def load_teachers_classes():
    """Load three rows into the teachers_classes association table"""

    print "Teachers_Classes"

    teacher_class = TeacherClass(teacher_id=1,
                                class_id=1,
                                permission_level="admin")
    db.session.add(teacher_class)
    db.session.commit()


# def load_movies():
#     """Load movies from u.item into database."""

#     print "Movies"

#     for i, row in enumerate(open("seed_data/u.item")):
#         row = row.rstrip()

#         # clever -- we can unpack part of the row!
#         movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

#         # The date is in the file as daynum-month_abbreviation-year;
#         # we need to convert it to an actual datetime object.

#         if released_str:
#             released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
#         else:
#             released_at = None

#         # Remove the (YEAR) from the end of the title.

#         title = title[:-7]   # " (YEAR)" == 7

#         movie = Movie(title=title,
#                       released_at=released_at,
#                       imdb_url=imdb_url)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(movie)

#         # provide some sense of progress
#         if i % 100 == 0:
#             print i

#     # Once we're done, we should commit our work
#     db.session.commit()


# def load_ratings():
#     """Load ratings from u.data into database."""

#     print "Ratings"

#     for i, row in enumerate(open("seed_data/u.data")):
#         row = row.rstrip()

#         user_id, movie_id, score, timestamp = row.split("\t")

#         user_id = int(user_id)
#         movie_id = int(movie_id)
#         score = int(score)

#         # We don't care about the timestamp, so we'll ignore this

#         rating = Rating(user_id=user_id,
#                         movie_id=movie_id,
#                         score=score)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(rating)

#         # provide some sense of progress
#         if i % 1000 == 0:
#             print i

#             # An optimization: if we commit after every add, the database
#             # will do a lot of work committing each record. However, if we
#             # wait until the end, on computers with smaller amounts of
#             # memory, it might thrash around. By committing every 1,000th
#             # add, we'll strike a good balance.

#             db.session.commit()

#     # Once we're done, we should commit our work
#     db.session.commit()


# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_teachers()
    load_subjects()
    load_classes()
    load_students()
    load_measures()
    load_teachers_classes()
  
    
    # set_val_user_id()
