# Blogs To Telegram

This GitHub Actions workflow automatically posts new articles from your DEV.to account to a specified Telegram chat. The workflow runs every hour and checks for new articles. If a new article is found, it sends a message to the Telegram chat with the article's title and URL.

## Features

- ✅ Automatic posting of new articles from DEV.to to Telegram
- ✅ Customizable message templates
- ✅ Batch posting of multiple articles
- ✅ Detailed logging and error handling
- ✅ Local development and testing support
- ✅ Comprehensive documentation

## Setup

1. **Fork the repository**: Fork this repository to your own GitHub account.

2. **Add Secrets**: Add the following secrets to your GitHub repository:
   - `DEVTO_API_KEY`: Your DEV.to API key.
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
   - `TELEGRAM_CHAT_ID`: The chat ID where you want to post the messages.

3. **Configure the Workflow**: The workflow is defined in `.github/workflows/post-to-telegram.yml`. It is scheduled to run every hour but can also be triggered manually.

For detailed setup instructions, see:

- [DEV.to API Setup Guide](docs/devto_api_setup.md)
- [Telegram Bot Setup Guide](docs/telegram_bot_setup.md)
- [Local Development Guide](LOCAL_DEVELOPMENT.md)

## How It Works

1. **Fetch DEV.to Articles**: The workflow fetches the latest published articles from your DEV.to account using the DEV.to API.

2. **Check for New Articles**: It compares the ID of the latest article with the ID stored in `last_posted_article_id.txt`. If they are different, it means a new article has been posted.

3. **Post to Telegram**: If a new article is found, the workflow sends a message to the specified Telegram chat with the article's title and URL.

4. **Update Last Posted Article ID**: The workflow updates the `last_posted_article_id.txt` file in the repository to keep track of the last posted article.

## Running the Workflow

The workflow runs automatically every hour. You can also trigger it manually from the Actions tab in your GitHub repository.

## Advanced Usage

For more advanced usage, including customizing message templates, batch posting, and local development, see the [Usage Guide](docs/usage_guide.md).

### Example Message

Here's an example of the default message that will be posted to Telegram:

```text
📝 *New DEV.to Article Published* 📝

*How to Automate Your Workflow with GitHub Actions*

🔗 [Read the full article](https://dev.to/yourusername/how-to-automate-your-workflow-with-github-actions)

Tags: #github #automation #workflow

⏱️ Reading time: 5 min

📅 Published on January 15, 2023

✍️ By Your Name
```

## Contributing

Feel free to contribute to this project and help make it better. You can create a pull request with your changes or open an issue if you have any questions or suggestions.

### Project Structure

```text
blogs-to-telegram/
├── .github/workflows/       # GitHub Actions workflows
├── docs/                    # Documentation
├── logs/                    # Log files (created at runtime)
├── src/                     # Source code
│   ├── advanced_post_to_telegram.py  # Advanced implementation
│   ├── devto_utils.py       # DEV.to API utilities
│   ├── enhanced_post_to_telegram.py  # Enhanced implementation
│   ├── env_loader.py        # Environment variable loader
│   ├── logging_utils.py     # Logging utilities
│   ├── message_formatter.py # Message formatting utilities
│   ├── post_to_telegram.py  # Basic implementation
│   └── telegram_utils.py    # Telegram API utilities
├── templates/               # Message templates
├── tools/                   # Utility scripts
│   ├── batch_post.py        # Batch posting tool
│   ├── manual_post.py       # Manual posting tool
│   └── validate_setup.py    # Setup validation tool
├── .env.sample              # Sample environment variables
├── .gitignore               # Git ignore file
├── config.json              # Configuration file
├── last_posted_article_id.txt  # Tracks the last posted article
├── LICENSE                  # License file
├── LOCAL_DEVELOPMENT.md     # Local development guide
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
