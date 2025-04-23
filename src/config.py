import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub Configuration
GH_TOKEN = os.getenv('GH_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
REPO_OWNER = os.getenv('REPO_OWNER')

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-pro'

# Application Configuration
COMMIT_TIME = os.getenv('COMMIT_TIME', '06:00')
AI_PROMPT = os.getenv('AI_PROMPT', 'Generate a thoughtful insight about technology trends for today.')
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PROMPT_TEMPLATE = """Provide a comprehensive analysis of current trends and insights for {date}. Include:
1. Major developments and their implications
2. Emerging trends and patterns
3. Future predictions and recommendations"""

REPORT_TEMPLATE = '''# Daily AI Insights Report
Generated on: {date}

## Today's Analysis
{content}

## Topic-Specific Insights
{topic_insights}

## Model Information
Generated using: {model}
Timestamp: {timestamp}
'''

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Schedule Configuration
SCHEDULE_TIME = "00:00"  # Run at midnight every day