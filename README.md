# AI Insights Bot

A Python application that uses Gemini AI to generate insights and automatically commits them to GitHub. Currently configured to run every 2 minutes for testing purposes.

## Quick Deploy on Railway

1. Fork this repository
2. Go to [Railway](https://railway.app/)
3. Create new project → Deploy from GitHub repo
4. Add these environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `GH_TOKEN`: Your GitHub personal access token
   - `REPO_NAME`: Your GitHub repository name
   - `REPO_OWNER`: Your GitHub username

## Local Testing

1. Clone the repository
2. Create `.env` file with the above environment variables
3. Run:

```bash
pip install -r requirements.txt
python -m src.main
```

## How it Works

1. Fetches AI insights using Gemini API
2. Generates a markdown report
3. Commits to your GitHub repository
4. Repeats every 2 minutes (for testing)

## Note

Currently set to run every 2 minutes for testing. To change this, modify the schedule in `src/main.py`.

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key
- `GH_TOKEN`: GitHub personal access token
- `REPO_NAME`: GitHub repository name
- `REPO_OWNER`: GitHub username

## Features

- Daily news fetching from multiple sources
- Sentiment analysis of news articles
- Topic extraction and trending analysis
- Automatic GitHub commits
- Fully automated using GitHub Actions
- No manual intervention needed

## Setup

1. Create a new GitHub repository
2. Clone this repository and push it to your new GitHub repository
3. Set up GitHub Secrets:
   - Go to your repository's Settings > Secrets and Variables > Actions
   - Add these secrets:
     - `NEWS_API_KEY`: Your NewsAPI key from https://newsapi.org
     - `GH_TOKEN`: Personal access token with repo permissions (classic)

That's it! The bot will automatically:

- Run daily at midnight UTC
- Create a new analysis report
- Commit it to your repository in the `reports` directory

## Manual Setup (Optional)

If you want to run the bot locally for testing:

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:

```
GH_TOKEN=your_github_token
REPO_NAME=your_repository_name
REPO_OWNER=your_github_username
NEWS_API_KEY=your_newsapi_key
```

4. Run the bot:

```bash
python src/main.py
```

## How It Works

The bot is automated using GitHub Actions:

1. Runs daily at midnight UTC
2. Fetches top news from configured sources
3. Performs sentiment analysis and topic extraction
4. Generates a markdown report
5. Automatically commits the report to your repository

You can also manually trigger the workflow:

1. Go to your repository's Actions tab
2. Select "Daily News Analysis" workflow
3. Click "Run workflow"

## Report Structure

Each daily report includes:

- Top headlines
- Sentiment analysis
- Key topics and trends
- Daily summary

## Configuration

Edit `src/config.py` to customize:

- News sources
- Report template
- Other settings

## Requirements

- GitHub account
- NewsAPI account (free tier)

## License

MIT License
