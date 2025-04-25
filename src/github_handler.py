from github import Github
from src.config import GH_TOKEN
from datetime import datetime
import os
import logging
from src.config import GH_TOKEN as GITHUB_TOKEN, REPO_NAME, REPO_OWNER

logger = logging.getLogger(__name__)

class GitHubHandler:
    def __init__(self):
        self.github = Github(GH_TOKEN)
        try:
            # Handle both formats: owner/repo or just repo name
            if '/' in REPO_NAME:
                repo_path = REPO_NAME
            else:
                repo_path = f"{REPO_OWNER}/{REPO_NAME}"
                
            logger.info(f"Attempting to access repository: {repo_path}")
            self.repo = self.github.get_repo(repo_path)
            logger.info("Successfully connected to repository")
        except Exception as e:
            logger.error(f"Failed to access repository {repo_path}: {str(e)}")
            logger.info("Please verify:")
            logger.info("1. The repository exists at github.com/{repo_path}")
            logger.info("2. The GitHub token has access to the repository")
            logger.info("3. The repository name and owner are correct in .env file")
            raise

    def commit_report(self, report_content):
        """Commit the daily report to GitHub"""
        try:
            # Use a single file for all reports
            file_path = 'reports/daily-analysis.md'

            try:
                # Try to get the file content first
                file = self.repo.get_contents(file_path)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Append the new report to the existing content
                try:
                    current_content = file.decoded_content.decode('utf-8')
                except:
                    current_content = ""
                
                # Add a separator between reports
                separator = "\n\n---\n\n"
                new_content = current_content + separator + report_content if current_content else report_content
                
                self.repo.update_file(
                    file_path,
                    f"Update news analysis report at {timestamp}",
                    new_content,
                    file.sha
                )
            except Exception:
                # File doesn't exist, create it
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.repo.create_file(
                    file_path,
                    f"Add news analysis report at {timestamp}",
                    report_content
                )

            logger.info(f"Successfully committed report at {timestamp}")
            return True

        except Exception as e:
            logger.error(f"GitHub commit error: {str(e)}", exc_info=True)
            return False

    def ensure_report_directory(self):
        """Ensure the reports directory exists in the repository"""
        logger.info("Verifying reports directory existence")
        try:
            try:
                self.repo.get_contents("reports")
                logger.debug("Reports directory already exists")
            except Exception:
                logger.info("Creating reports directory")
                self.repo.create_file(
                    "reports/.gitkeep",
                    "Initialize reports directory",
                    ""
                )
            return True
        except Exception as e:
            print(f"Error creating reports directory: {str(e)}")
            return False