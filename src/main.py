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

def run_task():
    """Run the task to fetch data from Gemini API and commit to GitHub"""
    logger.info(f"Starting task at {datetime.now()}")
    
    try:
        # Initialize components
        gemini_fetcher = GeminiFetcher()
        github_handler = GitHubHandler()

        # Ensure GitHub repository is properly set up
        github_handler.ensure_report_directory()

        # Fetch insights from Gemini API
        insights = gemini_fetcher.fetch_daily_insights()
        if not insights:
            logger.error("No insights fetched from Gemini API. Skipping.")
            return

        # Generate report
        report = REPORT_TEMPLATE.format(
            date=datetime.now().strftime('%Y-%m-%d %H:%M'),
            content=insights['content'],
            topic_insights="Generated every 2 minutes for testing",
            model=insights['model'],
            timestamp=insights['timestamp']
        )
        
        # Commit to GitHub
        success = github_handler.commit_report(report)
        
        if success:
            logger.info("Task completed successfully")
        else:
            logger.error("Failed to commit the report to GitHub")

    except Exception as e:
        logger.error(f"Error in task: {str(e)}")
        logger.exception("Full error details:")

if __name__ == "__main__":
    logger.info("Starting application with 2-minute intervals for testing")
    
    # Run immediately on startup
    run_task()
    
    # Schedule to run every 2 minutes
    schedule.every(2).minutes.do(run_task)
    
    # Keep the process running
    while True:
        schedule.run_pending()
        time.sleep(30)  # Check every 30 seconds