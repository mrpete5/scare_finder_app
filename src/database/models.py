from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'

    tmdb_id = db.Column(db.Integer, primary_key=True)  # TMDb movie ID
    imdb_id = db.Column(db.String(15), nullable=True)  # IMDb movie ID
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.String(10), nullable=True)  # YYYY-MM-DD
    poster_url = db.Column(db.String(255), nullable=True)
    overview = db.Column(db.Text, nullable=True)
    genres = db.Column(db.Text, nullable=True)  # JSON string of genres
    popularity = db.Column(db.Float, nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    tagline = db.Column(db.String(255), nullable=True)
    original_language = db.Column(db.String(10), nullable=True)
    imdb_rating = db.Column(db.Float, nullable=True)  # IMDb rating
    rotten_tomatoes_rating = db.Column(db.String(10), nullable=True)  # Rotten Tomatoes rating
    metacritic_score = db.Column(db.String(10), nullable=True)  # Metacritic score
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Tracks last full update

    # Relationship to StreamingProvider
    providers = db.relationship('StreamingProvider', backref='movie', lazy=True)

class StreamingProvider(db.Model):
    __tablename__ = 'streaming_providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Provider name
    logo_url = db.Column(db.String(255), nullable=True)  # URL for the logo
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.tmdb_id'), nullable=False)  # Link to Movie

def init_db(app):
    """Initializes the database with the Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()