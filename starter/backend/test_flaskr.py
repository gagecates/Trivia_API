import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who was the first President of the United States?',
            'answer': 'George Washington',
            'difficulty': 1,
            'category': '3'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    # after each test revert changes
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_add_question(self):

        
        # record number of current questions 
        number_questions = len(Question.query.all())

        # add new question to table
        res = self.client().post('questions/add', json=self.new_question)
        data = json.loads(res.data)

        # record number of current questions after adding new
        number_questions_new = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(number_questions_new, number_questions +1)

    def test_delete_question(self):

        # create a new question to be deleted
        question = Question(
                question="What's new?",
                answer="Not much",
                difficulty=1,
                category=3,
            )

        # add new question to table
        question.insert()
        question_id = question.id

        # record number of questions before delete
        number_questions = len(Question.query.all())


        # delete new question
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        # record number of questions after delete
        number_questions_new = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(number_questions_new, number_questions -1)


    def test_question_search_404(self):

        # test using a funky entry for a search
        search_terms = {
            'searchTerm': '8675309',
        }

        res = self.client().post('/questions/search', json=search_terms)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_page_out_of_range_400(self):

        # send request for out of range page number
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)

        # check response status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

# Make the tests conveniently executable

if __name__ == "__main__":
    unittest.main()