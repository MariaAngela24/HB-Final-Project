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
                    username="mariamendiburo@gmail.com")
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
        first_name, last_name, grade, gender, username, math_placement, reading_grade_equivalent = row.split("|")
        student = Student(
                        first_name=first_name, 
                        last_name=last_name, 
                        grade=grade, 
                        gender=gender, 
                        username=username, 
                        math_placement=math_placement, 
                        reading_grade_equivalent=reading_grade_equivalent)

        db.session.add(student)
        db.session.commit()



def load_measures():
    """Load rows into the measures table."""

    print "Measures"

    for i, row in enumerate(open("seed_data/u.measure.txt")):
        row = row.rstrip()
        class_id, flag, status = row.split("|")
        measure = Measure(class_id=class_id, 
                        flag=flag,
                        #TO DO: Add datetime
                        status=status) 
                        
        db.session.add(measure)
        db.session.commit()



def load_teachers_classes():
    """Load rows into the teachers_classes association table"""

    print "Teachers_Classes"

    for i, row in enumerate(open("seed_data/u.teacher_class.txt")):
        row = row.rstrip()
        teacher_id, class_id, permission_level = row.split("|")
        teacher_class = TeacherClass(teacher_id=teacher_id, 
                    class_id=class_id) 
                        
        db.session.add(teacher_class)
        db.session.commit()



def load_students_classes():
    """Load rows into the students_classes association table"""

    print "Students_Classes"

    for i, row in enumerate(open("seed_data/u.student_class.txt")):
        row = row.rstrip()
        student_id, class_id = row.split("|")
        student_class = StudentClass(student_id=student_id, 
                                    class_id=class_id) 
                        
        db.session.add(student_class)
        db.session.commit()



def load_students_measures():
    """Load rows into the students_measures association table"""

    print "Students_Measures"

    for i, row in enumerate(open("seed_data/u.student_measure.txt")):
        row = row.rstrip()
        student_id, measure_id = row.split("|")
        student_measure = StudentMeasure(student_id=student_id, 
                                        measure_id=measure_id) 
                        
        db.session.add(student_measure)
        db.session.commit()



def load_objectives():
    """Load rows into the objectives table"""

    print "Objectives"

    for i, row in enumerate(open("seed_data/u.objective.tsv")):
        row = row.rstrip()
        objective_number, name, description, class_id = row.split("\t")
        objective = Objective(objective_number=objective_number,
                            name=name,
                            description=description,
                            class_id=class_id)
                                              
        db.session.add(objective)
        db.session.commit()



def load_questions():
    """Load survey questions into table"""

    print "Questions"

    for i, row in enumerate(open("seed_data/u.question.txt")):
        row = row.rstrip()
        measure_id, objective_id, prompt, flag, question_type, position = row.split("|")
        question = Question(measure_id=measure_id, 
                            objective_id=objective_id,
                            prompt=prompt,
                            flag=flag,
                            question_type=question_type,
                            position=position) 
                        
        db.session.add(question)
        db.session.commit()

    

def load_answers_choices():
    """Load answer choices into table"""

    print "Answers_Choices"

    for i, row in enumerate(open("seed_data/u.answer_choice.txt")):
        row = row.rstrip()
        text, value, position = row.split("|")
        answer_choice = AnswerChoice(text=text,
                                    value=value,
                                    position=position) 
                        
        db.session.add(answer_choice)
        db.session.commit()



def load_questions_answers_choices():
    """Load answer choices into table"""

    print "Questions_Answers_Choices"

    for i, row in enumerate(open("seed_data/u.question_answer_choice.txt")):
        row = row.rstrip()
        question_id, answer_choice_id = row.split("|")
        question_answer_choice = QuestionAnswerChoice(question_id=question_id,
                                                    answer_choice_id = answer_choice_id) 
                        
        db.session.add(question_answer_choice)
        db.session.commit()
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
    load_students_classes()
    load_students_measures()
    load_objectives()
    load_questions()
    load_answers_choices()
    load_questions_answers_choices()


  
  
    
    # set_val_user_id()
