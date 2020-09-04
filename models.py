from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate

database_name = "guru99"
database_path = 'postgres://izveqfdssnenxe:02e9028a505d6fd529db5ac3db62d01eceebc6c8fd3a9858ebe98bdcdead9a97@ec2-34-232-212-164.compute-1.amazonaws.com:5432/d687ma0qdnn95q'
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))
    movies = db.relationship(
        'Movie',
        secondary='has'
    )

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    start_time = db.Column(db.DateTime, default=db.func.now())

    actors = db.relationship(
        'Actor',
        secondary='has'
    )

    def __init__(self, title, start_time):
        self.title = title
        self.start_time = start_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time
        }


class Has(db.Model):
    __tablename__ = 'has'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey(Actor.id))
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    actor = db.relationship(Actor, backref=db.backref("actor_assoc"))
    movie = db.relationship(Movie, backref=db.backref("movie_assoc"))
