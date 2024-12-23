import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "Authorization": f"Bearer {TMDB_API_KEY}",
    "accept": "application/json"
}

def fetch_popular_movies(page):
    url = f"{BASE_URL}/movie/popular?language=en-US&page={page}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

def fetch_movie_details_and_providers(tmdb_id):
    url = f"{BASE_URL}/movie/{tmdb_id}?language=en-US&append_to_response=watch/providers"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for TMDb ID {tmdb_id}: {response.status_code}")
        return None
