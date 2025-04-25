import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub Configuration
GH_TOKEN = os.getenv('GH_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
REPO_OWNER = os.getenv('REPO_OWNER')

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-pro'

# Prompt Template
PROMPT_TEMPLATE = """Generate a thoughtful insight about current technology trends and developments. Include:
1. Major developments and their implications
2. Emerging trends and patterns
3. Future predictions and recommendations"""

# Report Template
REPORT_TEMPLATE = '''# AI Insights Report
Generated on: {date}

## Analysis
{content}

## Additional Notes
{topic_insights}

## Generation Info
Model: {model}
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