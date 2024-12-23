import unittest
from unittest.mock import patch, MagicMock
from src.data_collection.fetch_tmdb import fetch_movie_details_and_providers
from src.data_collection.fetch_omdb import fetch_omdb_data


class TestTMDbAPI(unittest.TestCase):
    @patch('src.data_collection.fetch_tmdb.requests.get')
    def test_fetch_movie_details_and_providers(self, mock_get):
        # Mock TMDb API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 123,
            "title": "Mock Movie",
            "genres": [{"name": "Horror"}],
            "release_date": "2023-01-01",
            "watch/providers": {
                "US": {
                    "flatrate": [
                        {
                            "provider_name": "Netflix",
                            "logo_path": "/mock_logo.jpg"
                        }
                    ]
                }
            },
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the function
        movie_data = fetch_movie_details_and_providers(123)

        # Assertions
        self.assertEqual(movie_data["id"], 123)
        self.assertEqual(movie_data["title"], "Mock Movie")
        self.assertEqual(movie_data["watch/providers"]["US"]["flatrate"][0]["provider_name"], "Netflix")


class TestOMDbAPI(unittest.TestCase):
    @patch('src.data_collection.fetch_omdb.requests.get')
    def test_fetch_omdb_data(self, mock_get):
        # Mock OMDb API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "imdbID": "tt1234567",
            "imdbRating": "7.5",
            "Ratings": [
                {"Source": "Rotten Tomatoes", "Value": "85%"}
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the function
        omdb_data = fetch_omdb_data("tt1234567")

        # Assertions
        self.assertEqual(omdb_data["imdbID"], "tt1234567")
        self.assertEqual(omdb_data["imdbRating"], "7.5")
        self.assertEqual(omdb_data["Ratings"][0]["Source"], "Rotten Tomatoes")
        self.assertEqual(omdb_data["Ratings"][0]["Value"], "85%")


if __name__ == "__main__":
    unittest.main()
