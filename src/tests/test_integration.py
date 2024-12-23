import unittest
from flask import Flask
from src.web_app.app import app, fetch_movies_from_db

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the index route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Scare Finder", response.data)  # Check page content

    def test_update_route(self):
        """Test the update route."""
        response = self.app.get('/update')
        self.assertEqual(response.status_code, 302)  # Expecting redirect to home

    def test_fetch_movies_from_db(self):
        """Test fetch_movies_from_db returns data."""
        movies = fetch_movies_from_db()
        self.assertIsInstance(movies, list)

if __name__ == "__main__":
    unittest.main()
