from datetime import datetime
from news_fetcher import NewsFetcher
from analyzer import NewsAnalyzer
from github_handler import GitHubHandler

import schedule
import time

def run_daily_analysis():
    """Run the daily AI insights analysis and commit to GitHub"""
    logger.info(f"Starting daily analysis at {datetime.now()}")
    
    try:
        # Initialize components
        gemini_fetcher = GeminiFetcher()
        github_handler = GitHubHandler()

        # Ensure GitHub repository is properly set up
        github_handler.ensure_report_directory()

        # Fetch daily insights
        insights = gemini_fetcher.fetch_daily_insights()
        if not insights:
            print("No insights fetched. Skipping analysis.")
            return

        # Fetch additional topic insights
        topics = ["AI and Technology", "Global Economy", "Climate Change"]
        topic_insights = []
        for topic in topics:
            topic_result = gemini_fetcher.fetch_topic_insights(topic)
            if topic_result:
                topic_insights.append(topic_result)
        
        # Generate report
        report = REPORT_TEMPLATE.format(
            date=datetime.now().strftime('%Y-%m-%d'),
            content=insights['content'],
            topic_insights='\n'.join([f"### {t['topic']}\n{t['content']}" for t in topic_insights]),
            model=insights['model'],
            timestamp=insights['timestamp']
        )
        
        # Commit to GitHub
        success = github_handler.commit_report(report)
        
        if success:
            print("Daily AI insights analysis completed successfully")
        else:
            print("Failed to commit the report to GitHub")

    except Exception as e:
        print(f"Error in daily analysis: {str(e)}")
        raise e  # Re-raise the exception to make GitHub Actions mark the run as failed

if __name__ == "__main__":
    # Initialize logging
    from config import LOGGING_CONFIG
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Schedule daily job
    schedule.every(1).minutes.do(run_daily_analysis)
    logger.info(f"Scheduled analysis to run daily at {os.getenv('COMMIT_TIME', '06:00')}")
    
    # Keep process running
    while True:
        schedule.run_pending()
        time.sleep(60)