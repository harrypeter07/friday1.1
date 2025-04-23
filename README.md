# Automated News Analysis Bot

This bot automatically fetches daily news, performs analysis, and commits the results to GitHub. It runs completely autonomously using GitHub Actions.

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
   - Add the following secret:
     - `NEWS_API_KEY`: Your NewsAPI key from https://newsapi.org

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
GITHUB_TOKEN=your_github_token
GITHUB_REPO=your_repository_name
GITHUB_USERNAME=your_github_username
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
