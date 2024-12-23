# Scare Finder Web App

Scare Finder is a web application that helps users discover horror movies available on popular streaming platforms. The app provides movie details such as title, release date, IMDb rating, genres, and streaming providers. Users can filter movies by streaming provider and update the database with the latest information.

## Prerequisites

- Python 3.8 or above
- Virtual environment (optional but recommended)
- Required Python libraries listed in `requirements.txt`

## Getting Started

1. Clone the repository and navigate to the project directory.

    `git clone <repository-url>`
   
    `cd <repository-folder>`
3. Set up a virtual environment (optional but recommended):
   - For Linux/Mac: `python -m venv venv && source venv/bin/activate`
   - For Windows: `python -m venv venv && venv\Scripts\activate`
4. Install dependencies using `pip install -r requirements.txt`.
5. Create a `.env` file in the project directory and add your TMDb and OMDb API keys:

    `TMDB_API_KEY=<your_tmdb_api_key>`

    `OMDB_API_KEY=<your_omdb_api_key>`
7. Start the web app with `flask run` and open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Features

- View a list of horror movies with their details, including streaming providers.
- Filter movies by a specific streaming provider.
- Update the database with new movie data.
