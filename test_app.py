import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor


class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.test_database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.test_database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            self.correct_actor = {
                'name': 'ahmed',
                'age': 10,
                'gender': 'man',
            }
            self.uncorrect_actor = {
                'name': 'ahmed',
                'age': '',
                'gender': 'man',
            }
            self.correct_movie = {
                'title': 'this is a trivia question',
            }
            self.uncorrect_movie = {
                'title': '',
            }
            self.producer_token = os.environ['producer']
            self.director_casting_token = os.environ['director']
            self.assistant_casting_token = os.environ['assistant']

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_available_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_casting_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_available_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_casting_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_delete_actor(self):
        res = self.client().delete('/actors/9', headers={
            'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        q = Actor.query.get(9)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(q, None)
        self.assertTrue(data['actors'])

    def test_404_can_not_delete_actor(self):
        res = self.client().delete('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        q = Movie.query.get(3)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(q, None)
        self.assertTrue(data['movies'])

    def test_404_can_not_delete_movie(self):
        res = self.client().delete('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_actor(self):
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        },
            json=self.correct_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_create_movie(self):
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        },
            json=self.correct_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_422_if_actor_creation_fails(self):
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        },
            json=self.uncorrect_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_movie_creation_fails(self):
        res = self.client().post('/movies',  headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        },
            json=self.uncorrect_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_movie(self):
        res = self.client().patch('/movies/6', headers={
            'Authorization': "Bearer {}".format(self.director_casting_token)
        },
           json=self.correct_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_update_movie(self):
        res = self.client().patch('/movies/70', headers={
            'Authorization': "Bearer {}".format(self.director_casting_token)
        },
             json=self.correct_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        res = self.client().patch('/actors/4', headers={
            'Authorization': "Bearer {}".format(self.director_casting_token)
        },
             json=self.correct_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_update_actor(self):
        res = self.client().patch('/actors/70', headers={
            'Authorization': "Bearer {}".format(self.director_casting_token)
        },
            json=self.correct_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
