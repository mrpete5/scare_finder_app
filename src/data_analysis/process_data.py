import json
from datetime import datetime
from src.database.models import db, Movie, StreamingProvider
from src.data_collection.fetch_tmdb import fetch_movie_details_and_providers, fetch_popular_movies
from src.data_collection.fetch_omdb import fetch_omdb_data

ALLOWED_PROVIDERS = [
    "Netflix", "Hulu", "Amazon Prime Video", "Disney Plus", 
    "MUBI", "Max", "Paramount Plus", "Peacock Premium", 
    "Shudder", "Starz"
]

def parse_streaming_providers(provider_data):
    """Parse and filter streaming providers, including their logos, for the US region."""
    if not provider_data or "US" not in provider_data:
        # print("No provider data for US region.")  # Debug log
        return []

    parsed_providers = []
    us_providers = provider_data["US"].get("flatrate", [])
    
    for provider in us_providers:
        # print("Processing provider:", provider)  # Debug log
        if provider["provider_name"] in ALLOWED_PROVIDERS:
            parsed_providers.append({
                "name": provider["provider_name"],
                "logo_url": f"https://image.tmdb.org/t/p/w200{provider['logo_path']}"
            })

    # print("Parsed providers:", parsed_providers)  # Debug log
    return parsed_providers

def save_movie_to_db(movie_data, omdb_data=None, update_type="full"):
    """Saves or updates movie data and its streaming providers in the database."""
    # print(f"Processing movie: {movie_data.get('title')} (TMDb ID: {movie_data.get('id')})")  # Debug log

    # Fetch existing movie if available
    movie = Movie.query.filter_by(tmdb_id=movie_data['id']).first()

    def parse_rating(rating):
        try:
            return float(rating)
        except (ValueError, TypeError):
            return None

    if not movie:
        # New movie entry
        movie = Movie(
            tmdb_id=movie_data['id'],
            imdb_id=movie_data.get('imdb_id'),
            title=movie_data['title'],
            release_date=movie_data.get('release_date'),
            poster_url=movie_data.get('poster_path'),
            overview=movie_data.get('overview'),
            genres=json.dumps([genre['name'] for genre in movie_data.get('genres', [])]),
            popularity=movie_data.get('popularity'),
            runtime=movie_data.get('runtime'),
            tagline=movie_data.get('tagline'),
            original_language=movie_data.get('original_language'),
            imdb_rating=parse_rating(omdb_data.get('imdbRating')) if omdb_data else None,
            rotten_tomatoes_rating=next((r['Value'] for r in omdb_data.get('Ratings', []) if r['Source'] == 'Rotten Tomatoes'), None) if omdb_data else None,
            metacritic_score=next((r['Value'] for r in omdb_data.get('Ratings', []) if r['Source'] == 'Metacritic'), None) if omdb_data else None,
        )
        db.session.add(movie)
    else:
        # Update existing movie
        if update_type == "full":
            movie.title = movie_data['title']
            movie.release_date = movie_data.get('release_date')
            movie.poster_url = movie_data.get('poster_path')
            movie.overview = movie_data.get('overview')
            movie.genres = json.dumps([genre['name'] for genre in movie_data.get('genres', [])])
            movie.popularity = movie_data.get('popularity')
            movie.runtime = movie_data.get('runtime')
            movie.tagline = movie_data.get('tagline')
            movie.original_language = movie_data.get('original_language')

    # Clear existing providers
    # print(f"Clearing existing providers for movie: {movie_data['title']}")  # Debug log
    StreamingProvider.query.filter_by(movie_id=movie.tmdb_id).delete()

    # Add streaming providers
    us_provider_data = movie_data.get('watch/providers', {}).get('results', {}).get('US', {}).get('flatrate', [])
    # print(f"US Flatrate Providers: {us_provider_data}")  # Debug log

    for provider in us_provider_data:
        if provider['provider_name'] in ALLOWED_PROVIDERS:
            # print(f"Adding provider: {provider['provider_name']} for movie {movie_data['title']}")  # Debug log
            new_provider = StreamingProvider(
                name=provider['provider_name'],
                logo_url=f"https://image.tmdb.org/t/p/w200{provider['logo_path']}",
                movie_id=movie.tmdb_id
            )
            db.session.add(new_provider)

    db.session.commit()
    print(f"Processed movie: {movie_data['title']} (TMDb ID: {movie_data['id']})")


def process_movies(update_type="full", pages=20):
    """Processes movies, either fully or partially updating."""
    for page in range(1, pages+1):  # Fetch pages of popular movies
        popular_movies = fetch_popular_movies(page)
        if popular_movies:
            for movie in popular_movies['results']:
                if 27 in movie['genre_ids']:  # Horror genre ID
                    movie_data = fetch_movie_details_and_providers(movie['id'])
                    # print("Fetched movie data:", json.dumps(movie_data, indent=2))  # Debug log
                    omdb_data = None
                    if not Movie.query.filter_by(tmdb_id=movie_data['id']).first() or update_type == "full":
                        omdb_data = fetch_omdb_data(movie_data.get('imdb_id')) if movie_data.get('imdb_id') else None
                    save_movie_to_db(movie_data, omdb_data, update_type=update_type)
