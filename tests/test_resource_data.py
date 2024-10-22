import unittest
from unittest.mock import patch, Mock
from eprints_fetcher import EprintsDataFetcher

class TestResourceDataFetcher(unittest.TestCase):
    @patch('eprints_fetcher.requests.get')  # Mocking the requests.get method
    def test_fetch_and_process_data_success(self, mock_get):
        # Mock a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"title": "Test Title", "date": "2023-01-01", "creators": [{"nim": "12345", "name": {"given": "John", "family": "Doe"}}], "contributors": [{"name": {"given": "Jane", "family": "Smith"}}]}'
        mock_get.return_value = mock_response

        fetcher = EprintsDataFetcher(["https://fakeurl.com"])
        data = fetcher.fetch_and_process_data("https://fakeurl.com")

        # Assert that the fetched data is parsed correctly
        self.assertIsNotNone(data)
        self.assertEqual(data['title'], "Test Title")
        self.assertEqual(data['date'], "2023-01-01")

if __name__ == '__main__':
    unittest.main()