import os
import sys
import unittest
from unittest.mock import patch, Mock

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from tools.web_scrapper.src.web_scraper import web_scraper
from tools.web_scrapper.deployment.app import scrape_and_display

class TestWebScraper(unittest.TestCase):
    def setUp(self):
        # Setup a valid URL and API key for the tests
        self.url = 'https://www.robots.ox.ac.uk/~vgg/data/flowers/102/categories.html'
        self.api_key = 'test-api-key'

    @patch('tools.web_scrapper.src.web_scraper.requests.get')  # Correct patching path
    def test_web_scraper_success(self, mock_get):
        # Mock a successful response from the requests.get call
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Sample scraped content'
        mock_get.return_value = mock_response

        # Call the web_scraper function with URL and API key
        result = web_scraper(self.url, self.api_key)

        # Update the expected call to match the actual one
        expected_url = 'https://r.jina.ai/' + self.url
        expected_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Locale": "en-US",
            "X-Return-Format": "markdown",
            "X-With-Generated-Alt": "true",
            "X-With-Links-Summary": "true"
        }

        # Check if requests.get was called with the correct URL and headers
        mock_get.assert_called_once_with(expected_url, headers=expected_headers)

        # Check the result from the function
        self.assertEqual(result, 'Sample scraped content')


    @patch('tools.web_scrapper.src.web_scraper.requests.get')  # Correct patching path
    def test_web_scraper_failure(self, mock_get):
        # Mock a failed response (e.g., 404 not found)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'
        mock_get.return_value = mock_response

        # Call the web_scraper function with URL and API key
        result = web_scraper(self.url, self.api_key)

        # Verify that the function returns the correct response
        self.assertEqual(result, 'Not Found')

    @patch('tools.web_scrapper.src.web_scraper.requests.get')  # Correct patching path
    def test_web_scraper_unauthorized(self, mock_get):
        # Mock an unauthorized response (e.g., 401 Unauthorized)
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Unauthorized'
        mock_get.return_value = mock_response

        # Call the web_scraper function with URL and API key
        result = web_scraper(self.url, self.api_key)

        # Check if the response text is 'Unauthorized'
        self.assertEqual(result, 'Unauthorized')

    @patch("tools.web_scrapper.deployment.app.requests.get")
    def test_scrape_and_display(self, mock_get):
        """
        Test scrape_and_display to ensure it scrapes the content and creates a temporary file.
        """
        # Mock response for requests.get
        mock_response = mock_get.return_value
        mock_response.text = "Mocked scraped content"

        # Call the scrape_and_display function
        url = "https://brainsparkd.com/blog/introduction-to-ai-a-hands-on-tutorial-with-fastai/"
        scraped_content, file_path = scrape_and_display(url)

        # Assert that the scraped content is correct
        self.assertEqual(scraped_content, "Mocked scraped content")

        # Assert that the temporary file was created
        self.assertTrue(os.path.exists(file_path))

        # Clean up temporary file after the test
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
