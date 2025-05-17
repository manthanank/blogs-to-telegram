# Local Development Environment

This project can be run locally for development and testing before deploying to GitHub Actions.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/manthanank/blogs-to-telegram.git
   cd blogs-to-telegram
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your credentials:

   ```bash
   DEVTO_API_KEY=your_devto_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   ```

## Usage

### Running the Script

```bash
To run the main script locally:

```bash
python src/post_to_telegram.py
```

Or you can use the enhanced version:

```bash
python src/enhanced_post_to_telegram.py
```

### Manual Posting

You can use the manual posting tool for testing:

```bash
python tools/manual_post.py
```

Optional arguments:

- `--article-id`: Post a specific article by ID
- `--force`: Force posting even if the article has already been posted
- `--dry-run`: Do not actually post to Telegram, just print the message

### Environment Variables

The following environment variables are required:

- `DEVTO_API_KEY`: Your DEV.to API key
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: The chat ID where you want to post the messages

## Testing

To test the script without actually posting to Telegram, use the `--dry-run` option:

```bash
python tools/manual_post.py --dry-run
```

## Customization

You can customize the message format and other settings by editing the `config.json` file in the root directory.
