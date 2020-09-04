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
        self.database_name = "guru99_test"
        self.database_path = 'postgres://shaker:a@localhost:5432/guru99_test'
        setup_db(self.app, self.database_path)

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
            self.producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImludFdtb3RwY0VEd3FQRk43a3Z1NyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rLXc0aC02aC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1MGNmMzQyYzM2ZmQwMDY3YzZmOGU1IiwiYXVkIjoiaW1hZ2UiLCJpYXQiOjE1OTkxNzIyMDQsImV4cCI6MTU5OTE3OTQwNCwiYXpwIjoiVHRJWDc3eFV6dmxwZ0NwNm9KckY2YkFlSTJJemcxaHYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IgIiwicGF0Y2g6bW92aWUiXX0.ELT0I6CGANTFcb3PNudq4R-CLmHS7EYDSO-I9q6sVxAFbAYSs2Zz1wcYPrVVUQTq7EniOulM4zJs93XtZZu2MbY83vMdODV6AHnBh6ROE0GpxvvPMYsQCnm4w0tcisZ2j1EYeL5QdD_nNVoPJYUHIuOhbYOMKBiZFDdZI-t887DACdUN3_4r3fpH_MWxG8Z6jnrVXpDvyo5io1NdiYHNhICOjBajzf9XFT5Qpo1n7VGKeQEunG4x7RESXIBQ7zt-sEdcM8e04--mh8bJga30XArKRv4A8ub7J_an4Si3W9ryzOhtkVWCzi5B4r7XgwzMtDyKO3w6unc3pzgAlEcudA'
            self.director_casting_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImludFdtb3RwY0VEd3FQRk43a3Z1NyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rLXc0aC02aC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1MGNmMzQyYzM2ZmQwMDY3YzZmOGU1IiwiYXVkIjoiaW1hZ2UiLCJpYXQiOjE1OTkxNzMzNTUsImV4cCI6MTU5OTE4MDU1NSwiYXpwIjoiVHRJWDc3eFV6dmxwZ0NwNm9KckY2YkFlSTJJemcxaHYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IgIiwicGF0Y2g6bW92aWUiXX0.gFoPJMZ4hGMTCtlLuOWZeTbPgs0BTNOoQTpIfVWB2AcvLThYL01cOupkGcwOFon8vjXMFB5aonttsSxXdnk1uS1o9tLZBBTLRORCdI35jOoE4eO-Ly5ianT6Zcjh8QDTOxykpad9gmYRMmszuOr1MJFatAso9BouwKSbNz22wc-p5nahQggXgXWZ460g9X1-b90aXQjALqjYdFZ0LujNkY9FWjU79U5R_76bA2pYbyLL0jM4gI9GH8ToIZIMIt5BqdWvGQwpaVUKSnpNh1S_i-L7dyulb7AWOcclEiUVID2pnCKet_o_WLtptiLD1Cz1e9w6fPMMOF5FWBoV-P944g'
            self.assistant_casting_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImludFdtb3RwY0VEd3FQRk43a3Z1NyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rLXc0aC02aC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1MGNmMzQyYzM2ZmQwMDY3YzZmOGU1IiwiYXVkIjoiaW1hZ2UiLCJpYXQiOjE1OTkxNzA3MTcsImV4cCI6MTU5OTE3NzkxNywiYXpwIjoiVHRJWDc3eFV6dmxwZ0NwNm9KckY2YkFlSTJJemcxaHYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.iFCsoeyy83b8z20zUZt6kIgZoLXKrCW3QoEs5wuTxVxi1PML5UVYbi7QqHwBo1VRwW2F4KmiUr_9jKGhG-kKehsCZ9r7S6T2L7EqLtjr35dLlZw5NC6kHAI1tAJG8LwU592qemFKaTf1scjAiajw--HMnDxEjDp_Q8HM-cGqTzbUGegtYKx6F8UDvSvJdwUVsmSOSNa80eXbT2vgkNNgXxWu8mUMXf0tLXZKL_Bi2JUmWfNsq575Bf2d8Rn7IUBtrXNuoho9TIv224ou-oiG7_GRZXbNe9y9kdZFmIUQRuMlMAU0XBKU3IlF2YP-4FnvlzC9PluyB3PWXyHd3uyWaA'

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_available_actors(self):
        res = self.client().get('/actors', headers={'Authorization': "Bearer {}".format(self.assistant_casting_token)
                                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_available_movies(self):
        res = self.client().get('/movies', headers={'Authorization': "Bearer {}".format(self.assistant_casting_token)
                                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_delete_actor(self):
        res = self.client().delete('/actors/9', headers={'Authorization': "Bearer {}".format(self.producer_token)
                                                         })
        data = json.loads(res.data)
        q = Actor.query.get(9)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(q, None)
        self.assertTrue(data['actors'])

    def test_404_can_not_delete_actor(self):
        res = self.client().delete('/actors/100', headers={'Authorization': "Bearer {}".format(self.producer_token)
                                                           })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/3', headers={'Authorization': "Bearer {}".format(self.producer_token)
                                                        })
        data = json.loads(res.data)
        q = Movie.query.get(3)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(q, None)
        self.assertTrue(data['movies'])

    def test_404_can_not_delete_movie(self):
        res = self.client().delete('/movies/100', headers={'Authorization': "Bearer {}".format(self.producer_token)
                                                           })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_actor(self):
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.producer_token)
                                                     }, json=self.correct_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie(self):
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.producer_token)
                                                     }, json=self.correct_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_actor_creation_fails(self):
        res = self.client().post('/actors', headers={'Authorization': "Bearer {}".format(self.producer_token)
                                                     }, json=self.uncorrect_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_movie_creation_fails(self):
        res = self.client().post('/movies', headers={'Authorization': "Bearer {}".format(self.producer_token)
                                                     }, json=self.uncorrect_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_movie(self):
        res = self.client().patch('/movies/6', headers={'Authorization': "Bearer {}".format(self.director_casting_token)
                                                        }, json=self.correct_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_movie(self):
        res = self.client().patch('/movies/70', headers={'Authorization': "Bearer {}".format(self.director_casting_token)
                                                        }, json=self.correct_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        res = self.client().patch('/actors/4', headers={'Authorization': "Bearer {}".format(self.director_casting_token)
                                                        }, json=self.correct_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_actor(self):
        res = self.client().patch('/actors/70', headers={'Authorization': "Bearer {}".format(self.director_casting_token)
                                                        }, json=self.correct_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
