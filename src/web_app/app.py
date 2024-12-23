import os
import sqlite3
import json
from flask import Flask, Blueprint, render_template, redirect, url_for, request
from src.data_analysis.process_data import process_movies
from src.database.models import db, init_db

# Flask App Setup
app = Flask(__name__)

# Database Path Configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'src/database/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Blueprint Setup
main = Blueprint('main', __name__)


def fetch_movies_from_db(selected_provider=None):
    conn = sqlite3.connect('src/database/movies.db')
    cursor = conn.cursor()

    # Base query with LEFT JOIN to include all providers
    query = """
        SELECT m.tmdb_id, m.title, m.release_date, m.poster_url, m.imdb_rating, 
               m.genres, m.overview, sp.name, sp.logo_url
        FROM movies m
        LEFT JOIN streaming_providers sp ON m.tmdb_id = sp.movie_id
    """

    # Filtering logic for selected provider
    if selected_provider:
        query += """
            WHERE m.tmdb_id IN (
                SELECT movie_id
                FROM streaming_providers
                WHERE name = ?
            )
        """
        cursor.execute(query, (selected_provider,))
    else:
        cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    # Process movies into a dictionary to group providers
    movie_dict = {}
    for row in rows:
        tmdb_id, title, release_date, poster_url, imdb_rating, genres, overview, provider_name, provider_logo = row

        # Parse genres JSON
        parsed_genres = []
        if genres:
            try:
                parsed_genres = json.loads(genres)
            except json.JSONDecodeError:
                parsed_genres = []

        # Add movie to dictionary
        if tmdb_id not in movie_dict:
            movie_dict[tmdb_id] = {
                "title": title,
                "release_date": release_date,
                "poster_url": poster_url,
                "imdb_rating": imdb_rating,
                "genres": parsed_genres,
                "providers": [],
                "overview": overview
            }

        # Add all providers for the movie
        if provider_name and provider_logo:
            movie_dict[tmdb_id]["providers"].append({
                "name": provider_name,
                "logo_url": provider_logo
            })

    # Convert dictionary to a list of movies
    movies = list(movie_dict.values())
    return movies


@main.route('/')
def index():
    """Render the homepage with movies fetched from the database."""
    selected_provider = request.args.get('provider')
    movies = fetch_movies_from_db(selected_provider)
    return render_template('index.html', movies=movies, selected_provider=selected_provider)


@main.route('/update', methods=['GET'])
def update_movies():
    """Trigger the update process for movies."""
    process_movies(update_type="full")  # Call the data processing function
    return redirect(url_for('main.index'))  # Redirect back to the home page


# Register Blueprint
app.register_blueprint(main)

# Initialize Database
init_db(app)

if __name__ == '__main__':
    # Heroku requires binding to $PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
