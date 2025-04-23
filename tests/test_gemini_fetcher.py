import unittest
import logging
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.gemini_fetcher import GeminiClient, GeminiFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestGeminiClient(unittest.TestCase):
    def setUp(self):
        logger.info('Setting up TestGeminiClient test case')

    def test_init_with_api_key(self):
        logger.info('Testing GeminiClient initialization with API key')
        api_key = "test_key"
        client = GeminiClient(api_key=api_key)
        self.assertEqual(client.current_model, "gemini-1.5-pro")
        self.assertIn("gemini-1.5-pro", client.available_models)
        logger.info('GeminiClient initialization test completed successfully')

    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_env_key'})
    def test_init_with_env_var(self):
        client = GeminiClient()
        self.assertEqual(client.current_model, "gemini-1.5-pro")

    def test_init_without_api_key(self):
        with self.assertRaises(ValueError):
            GeminiClient()

class TestGeminiFetcher(unittest.TestCase):
    def setUp(self):
        logger.info('Setting up TestGeminiFetcher test case')
        self.fetcher = GeminiFetcher()

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_fetch_daily_insights_success(self, mock_generate):
        logger.info('Testing fetch_daily_insights with successful response')
        mock_response = MagicMock()
        mock_response.text = "Test insights content"
        mock_generate.return_value = mock_response

        result = self.fetcher.fetch_daily_insights()
        print(result)
        logger.info(f'Received response from Gemini API: {result["content"]}')

        self.assertIsNotNone(result)
        self.assertEqual(result['content'], "Test insights content")
        self.assertEqual(result['model'], "gemini-1.5-pro")
        self.assertIn('timestamp', result)
        logger.info('Daily insights test completed successfully')

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_fetch_daily_insights_empty_response(self, mock_generate):
        logger.info('Testing fetch_daily_insights with empty response')
        mock_response = MagicMock()
        mock_response.text = ""
        mock_generate.return_value = mock_response

        result = self.fetcher.fetch_daily_insights()
        logger.warning('Received empty response from Gemini API')
        self.assertIsNone(result)
        logger.info('Empty response test completed successfully')

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_github_automation_query(self, mock_generate):
        logger.info('Testing github automation query')
        mock_response = MagicMock()
        expected_response = "GitHub Actions is recommended for automation. Key benefits include:\n1. Built-in CI/CD\n2. Easy workflow configuration\n3. Secure secret management"
        mock_response.text = expected_response
        mock_generate.return_value = mock_response

        prompt = "What are the best practices for GitHub repository automation?"
        logger.info(f'Sending prompt to Gemini API: {prompt}')
        result = self.fetcher.client.model.generate_content(prompt)

        self.assertEqual(result.text, expected_response)
        mock_generate.assert_called_once()
        logger.info('GitHub automation query test completed successfully')

    def tearDown(self):
        logger.info('Cleaning up test case')

if __name__ == '__main__':
    unittest.main()