import os
import logging.config
from datetime import datetime
from src.gemini_fetcher import GeminiFetcher
from src.github_handler import GitHubHandler
from src.config import REPORT_TEMPLATE

import schedule
import time

# Initialize logging
from src.config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run_daily_task():
    """Run the daily task to fetch data from Gemini API and commit to GitHub"""
    logger.info(f"Starting daily task at {datetime.now()}")
    
    try:
        # Initialize components
        gemini_fetcher = GeminiFetcher()
        github_handler = GitHubHandler()

        # Ensure GitHub repository is properly set up
        github_handler.ensure_report_directory()

        # Fetch daily insights from Gemini API
        insights = gemini_fetcher.fetch_daily_insights()
        if not insights:
            logger.error("No insights fetched from Gemini API. Skipping analysis.")
            return

        # Generate report
        report = REPORT_TEMPLATE.format(
            date=datetime.now().strftime('%Y-%m-%d'),
            content=insights['content'],
            topic_insights="No additional insights",
            model=insights['model'],
            timestamp=insights['timestamp']
        )
        
        # Commit to GitHub
        success = github_handler.commit_report(report)
        
        if success:
            logger.info("Daily task completed successfully")
        else:
            logger.error("Failed to commit the report to GitHub")

    except Exception as e:
        logger.error(f"Error in daily task: {str(e)}")
        raise e

if __name__ == "__main__":
    
    # Schedule daily job
    schedule.every(1).minutes.do(run_daily_task)
    logger.info(f"Scheduled task to run daily at {os.getenv('COMMIT_TIME', '06:00')}")
    
    # Keep process running
    while True:
        schedule.run_pending()
        time.sleep(60)