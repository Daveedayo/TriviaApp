import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'Daveed9258', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What track are taking at the moment', 'answer': 'Lesson 2', 'difficulty': 1, 'difficulty': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data.get('success'))
        self.assertTrue(len(data['categories']))

    def test_404_for_get_categories_fail(self):
        res = self.client().get('/categories/1xx')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data.get('success'))
        self.assertTrue(len(data['questions']))

    def test_404_for_get_questions_fail(self):
        res = self.client().get('/questions/1xx')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data.get('success'))
        self.assertTrue(len(data['questions'])) 

    def test_404_for_get_paginated_questions_fail(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_specific_question(self):
        res = self.client().get('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data.get('success')) 
#
    def test_delete_question(self):
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 23).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data.get('success'))

    def test_delete_question_fail(self):
        res = self.client().delete('/questions/1xx')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_create_new_question(self):
        new_question = {
            'question': 'What track are taking at the moment', 'answer': 'Lesson 2', 'difficulty': 1, 'difficulty': 1
        }

        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_400_for_create_new_question_fail(self):
        res = self.client().post("/questions/2xx", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_get_questions_by_term(self):
        search_term = {'searchTerm': 'title'}
        res = self.client().post('/questions/find', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_400_for_get_questions_by_term_fail(self):
        res = self.client().post('/questions/find')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_404_for_get_questions_by_category_fail(self):
        res = self.client().get('/categories/xxx/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404) 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()