import unittest
from unittest.mock import patch
from src.data_analysis.process_data import parse_streaming_providers

class TestUnit(unittest.TestCase):
    def test_parse_streaming_providers_empty(self):
        """Test parse_streaming_providers with no data."""
        result = parse_streaming_providers(None)
        self.assertEqual(result, [])

    def test_parse_streaming_providers_valid(self):
        """Test parse_streaming_providers with valid data."""
        provider_data = {
            "US": {
                "flatrate": [
                    {"provider_name": "Netflix", "logo_path": "/netflix_logo.jpg"},
                    {"provider_name": "Hulu", "logo_path": "/hulu_logo.jpg"}
                ]
            }
        }
        result = parse_streaming_providers(provider_data)
        expected = [
            {"name": "Netflix", "logo_url": "https://image.tmdb.org/t/p/w200/netflix_logo.jpg"},
            {"name": "Hulu", "logo_url": "https://image.tmdb.org/t/p/w200/hulu_logo.jpg"}
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
