#Line below cannot be run and is throwing as error. Does not recognize server
from server import app
import unittest 
from model import connect_to_db, db, example_data

class SurveyRenderTestCase(unittest.TestCase):

    #Need to set session here with a student id=1
    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        #TO DO: Figure out if secret key here needs to match secret key in server file
        app.config['SECRET_KEY'] = 'ABC'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['student_id'] = 1

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_survey_render(self):
        """Testing that the survey page renders correct HTML template"""


        client = app.test_client()
        app.config['TESTING'] = True
        result = client.get("end-of-class-survey/1")
        self.assertIn('<title>Map My Learning</title>', result.data)


if __name__ == '__main__':
    unittest.main()
# In model.py, see Testing Flask lecture for example of how to create example data 

