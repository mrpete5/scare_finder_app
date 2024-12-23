import requests
import os
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"

def fetch_omdb_data(imdb_id):
    url = f"{BASE_URL}?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
