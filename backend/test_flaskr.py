import os
import unittest
import json
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.app_context().push()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format( "postgres", "root", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question":"what is your favorite sport", "answer":"Badminton", "category":"6", "difficulty":"1"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertFalse(data['current_category'])
        self.assertTrue(data['categories'])

    def test_get_questions_invalid_pages(self):
        res = self.client().get('/questions?page=2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_delete_questions(self):
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    def test_delete_questions_for_invalid_id(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource cannot be processed')

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["created"])
        self.assertTrue(data['total_questions'])

    def test_create_questions_with_null(self):
        payload = {"question": None, "answer":"Badminton", "category":6, "difficulty":1}
        res = self.client().post('/questions', json=payload)
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource cannot be processed')

    def test_get_questions_search(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_get_question_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_get_question_by_category_not_found(self):
        res = self.client().get('/categories/2000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quizzz(self):
        res = self.client().post('/quizzes',
                                 json={'previousQuestions': [2,5],
                                       'quizCategory':
                                       {'id': '5'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_quizzz_unprocessed(self):
        res = self.client().post('/quizzes', json={'previousQuestions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource cannot be processed')

# Make the tests conveniently executable
if __name__ == "__main__":
    # app=create_app()
    unittest.main()