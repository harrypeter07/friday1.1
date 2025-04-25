import os
import logging.config
from datetime import datetime
from src.gemini_fetcher import GeminiFetcher
from src.github_handler import GitHubHandler
from src.config import REPORT_TEMPLATE
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import schedule
import time

# Initialize logging
from src.config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Service is running")

def run_http_server():
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Starting HTTP server on port {port}")
    server.serve_forever()

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
            topic_insights="Daily analysis - 40 updates per day",
            model=insights['model'],
            timestamp=insights['timestamp']
        )
        
        # Commit to GitHub
        success = github_handler.commit_report(report)
        
        if success:
            logger.info("Task completed successfully")
        else:
            logger.error("Failed to commit the report to GitHubg")

    except Exception as e:
        logger.error(f"Error in task: {str(e)}")
        logger.exception("Full error details:")

def run_scheduler():
    logger.info("Starting scheduler with exactly 40 daily commits")
    
    # Calculate the interval for 40 commits per day
    # 24 hours * 60 minutes = 1440 minutes per day
    # 1440 minutes / 40 commits = 36 minutes between commits
    
    # Run immediately on startup
    run_task()
    
    # Schedule to run every 36 minutes
    schedule.every(36).minutes.do(run_task)
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    # Start the HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Run the scheduler in the main thread
    run_scheduler()