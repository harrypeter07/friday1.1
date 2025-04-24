import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.config import GEMINI_API_KEY, PROMPT_TEMPLATE

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = GEMINI_API_KEY
            if api_key is None:
                raise ValueError("API key must be configured in environment variables")

        genai.configure(api_key=api_key)
        
        self.available_models = {
            "gemini-1.5-pro": "gemini-1.5-pro",
            "gemini-1.5-flash": "gemini-1.5-flash",
            "gemini-1.0-pro": "gemini-1.0-pro",
            "gemini-1.0-ultra": "gemini-1.0-ultra",
        }
        
        self.current_model = "gemini-1.5-pro"
        self.model = genai.GenerativeModel(self.current_model)
    
    def set_model(self, model_name: str) -> None:
        """
        Change the model being used.
        
        Args:
            model_name: Name or shorthand of the model to use
        """
        if model_name in self.available_models:
            model_name = self.available_models[model_name]
            self.current_model = model_name
            self.model = genai.GenerativeModel(model_name)
        else:
            raise ValueError(f"Model {model_name} not found. Available models: {list(self.available_models.keys())}")

class GeminiFetcher:
    def __init__(self, api_key: Optional[str] = None):
        self.client = GeminiClient(api_key=api_key)

    def fetch_daily_insights(self) -> Optional[Dict[str, Any]]:
        """Fetch daily insights from Gemini API"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            prompt = PROMPT_TEMPLATE.format(date=today)
            
            response = self.client.model.generate_content(prompt)
            
            if response.text:
                return {
                'content': response.text,
                'date': today,
                'model': self.client.current_model,
                'timestamp': datetime.now().isoformat()
            }
            else:
                print("Error: Empty response from Gemini")
                return None
        except Exception as e:
            print(f"Error fetching from Gemini: {str(e)}")
            return None

    def fetch_topic_insights(self, topic: str) -> Optional[Dict[str, Any]]:
        """Fetch insights about a specific topic"""
        try:
            prompt = f"Provide detailed insights about {topic}. Include current trends, challenges, and future implications."
            
            response = self.client.model.generate_content(prompt)
            
            if response.text:
                return {
                    'topic': topic,
                    'content': response.text,
                    'timestamp': datetime.now().isoformat(),
                    'model': self.client.current_model
                }
            else:
                print(f"Error: Empty response for topic {topic}")
                return None
        except Exception as e:
            print(f"Error fetching topic insights: {str(e)}")
            return None
    
    def ask_question(self, question: str, temperature: float = 0.7) -> Optional[Dict[str, Any]]:
        """
        Ask a specific question to Gemini
        
        Args:
            question: The question to ask
            temperature: Controls randomness (0.0-1.0)
            
        Returns:
            Dictionary with response data or None if there was an error
        """
        try:
            generation_config = {
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 64,
            }
            
            response = self.client.model.generate_content(
                question,
                generation_config=generation_config,
                max_output_tokens=2048
            )

            if response.text:
                return {
                    'question': question,
                    'answer': response.text,
                    'timestamp': datetime.now().isoformat(),
                    'model': self.client.current_model
                }
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

def test_gemini_response():
    """Test function to demonstrate Gemini API usage with a mock question"""
    try:
        print("Testing Gemini API with a mock question...")
        
        # Try to get API key from environment variable
        api_key = os.environ.get("GOOGLE_API_KEY")
        
        if not api_key:
            print("\nNo API key found in environment variables.")
            print("Please provide your Gemini API key to test:")
            api_key = input("> ").strip()
            
            if not api_key:
                print("No API key provided. Test canceled.")
                return
        
        # Initialize the fetcher with the API key
        fetcher = GeminiFetcher(api_key=api_key)
        
        # Test with a mock question
        mock_question = "What are the key differences between Gemini 1.5 Pro and Gemini 1.0 Pro models?"
        print(f"\nSending question to Gemini API: '{mock_question}'")
        
        response = fetcher.ask_question(mock_question)
        
        if response:
            print("\n=== Gemini Response ===")
            print(f"Model used: {response['model']}")
            print(f"Timestamp: {response['timestamp']}")
            print("\nAnswer:")
            print(response['answer'])
            print("======================")
        else:
            print("Failed to get a response from Gemini API.")
        
        # Test topic insights
        print("\nTesting topic insights...")
        topic = "artificial intelligence ethics"
        topic_insights = fetcher.fetch_topic_insights(topic)
        
        if topic_insights:
            print(f"\n=== Topic Insights: {topic} ===")
            print(f"Model used: {topic_insights['model']}")
            print(f"Timestamp: {topic_insights['timestamp']}")
            print("\nContent (first 500 chars):")
            print(topic_insights['content'][:500] + "...")
            print("======================")
        
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        print("Make sure you have installed the required package: pip install google-generativeai")

if __name__ == "__main__":
    test_gemini_response()