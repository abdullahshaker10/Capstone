from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
from models import Actor, Movie, setup_db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors')
    @requires_auth('get:actors')
    def reterive_actors():
        try:
            actors = Actor.query.all()
            formated_actors = {}
            for actor in actors:
                formated_actors[actor.id] = actor.format()
            return jsonify({
                'success': True,
                'actors': formated_actors
            })
        except:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/movies')
    @requires_auth('get:movies')
    def reterive_movies():
        try:
            movies = Movie.query.all()
            formated_movies = {}
            for movie in movies:
                formated_movies[movie.id] = movie.format()
            return jsonify({
                'success': True,
                'movies': formated_movies
            })
        except:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(actor_id):

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }), 404

        actor.delete()
        actors = Actor.query.all()
        formated_actors = {}
        for actor in actors:
            formated_actors[actor.id] = actor.format()
        return jsonify({
            'success': True,
            'actors': formated_actors
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(movie_id):

        movie = Movie.query.filter(
            Movie.id == movie_id
        ).one_or_none()
        if not movie:
            return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }), 404

        movie.delete()
        formated_movies = {}
        movies = Movie.query.all()
        for movie in movies:
            formated_movies[movie.id] = movie.format()
        return jsonify({
            'success': True,
            'movies': formated_movies
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def create_actor():

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if name == '' or age == '' or gender == '':
            return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422
        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True
            })
        except:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movie')
    def create_movie():
        try:
            body = request.get_json()
            title = body.get('title', None)
            start_time = body.get('start_time', None)
            if title == '' or start_time == '':
                return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                }), 422
            movie = Movie(title=title, start_time=start_time)

            movie.insert()
            return jsonify({
                'success': True
            })
        except:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor ')
    def update_actor(actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id
            ).one_or_none()
            if actor is None:
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }), 404

            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.update()
            return jsonify({
                'success': True
            })
        except:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id
            ).one_or_none()
            if movie is None:
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }), 404

            body = request.get_json()
            title = body.get('title', None)
            start_time = body.get('start_time', None)
            movie.name = title
            movie.age = start_time
            movie.update()
            return jsonify({
                'success': True
            })
        except:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }), 404

        @app.errorhandler(422)
        def unprocessable(error):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422

        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }), 400

        @app.errorhandler(500)
        def bad_request(error):
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

        @app.errorhandler(AuthError)
        def handle_auth_error(error):

            response = jsonify(error.error)
            response.status_code = error.status_code

            return response

    return app


APP = create_app()

if __name__ == '__main__':
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        APP.run(host='0.0.0.0', port=port)