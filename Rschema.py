from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/moviesall'
db = SQLAlchemy(app)
#db.create_all()

# Define association tables for many-to-many relationships
movie_genre = db.Table('movie_genre',
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True))

movie_actor = db.Table('movie_actor',
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                       db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True))

movie_technician = db.Table('movie_technician',
                            db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                            db.Column('technician_id', db.Integer, db.ForeignKey('technician.id'), primary_key=True))

# Define models
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year_of_release = db.Column(db.Integer)
    ratings = db.Column(db.Float)
    genres = db.relationship('Genre', secondary=movie_genre, backref=db.backref('movies', lazy='dynamic'))
    actors = db.relationship('Actor', secondary=movie_actor, backref=db.backref('movies', lazy='dynamic'))
    technicians = db.relationship('Technician', secondary=movie_technician, backref=db.backref('movies', lazy='dynamic'))

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# API routes
@app.route('/movies', methods=['GET'])
def get_movies():
    # Retrieve all movies
    movies = Movie.query.all()
    return jsonify([movie.serialize() for movie in movies])

@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    # Retrieve a specific movie
    movie = Movie.query.get(movie_id)
    if movie:
        return jsonify(movie.serialize())
    else:
        return jsonify({'message': 'Movie not found'}), 404

@app.route('/movies', methods=['POST'])
def add_movie():
    # Add a new movie
    data = request.json
    movie = Movie(name=data['name'],
                  year_of_release=data['year_of_release'],
                  ratings=data['ratings'])
    db.session.add(movie)
    db.session.commit()
    return jsonify({'message': 'Movie added successfully'}), 201

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    # Update an existing movie
    movie = Movie.query.get(movie_id)
    if movie:
        data = request.json
        movie.name = data.get('name', movie.name)
        movie.year_of_release = data.get('year_of_release', movie.year_of_release)
        movie.ratings = data.get('ratings', movie.ratings)
        db.session.commit()
        return jsonify({'message': 'Movie updated successfully'})
    else:
        return jsonify({'message': 'Movie not found'}), 404

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    # Delete an actor if not associated with any movies
    actor = Actor.query.get(actor_id)
    if actor:
        if not actor.movies:
            db.session.delete(actor)
            db.session.commit()
            return jsonify({'message': 'Actor deleted successfully'})
        else:
            return jsonify({'message': 'Actor is associated with movies, cannot delete'}), 400
    else:
        return jsonify({'message': 'Actor not found'}), 404


    #db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
