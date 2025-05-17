"""
Command-line interface for manually posting DEV.to articles to Telegram.
"""

import os
import sys
import argparse
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parents[1]))

from src.devto_utils import DevToClient
from src.telegram_utils import TelegramMessenger

def setup_argparse():
    """
    Set up command-line argument parsing
    """
    parser = argparse.ArgumentParser(
        description="Post DEV.to articles to Telegram"
    )
    
    parser.add_argument(
        "--devto-api-key",
        help="Your DEV.to API key (defaults to environment variable DEVTO_API_KEY)"
    )
    
    parser.add_argument(
        "--telegram-bot-token",
        help="Your Telegram bot token (defaults to environment variable TELEGRAM_BOT_TOKEN)"
    )
    
    parser.add_argument(
        "--telegram-chat-id",
        help="Your Telegram chat ID (defaults to environment variable TELEGRAM_CHAT_ID)"
    )
    
    parser.add_argument(
        "--article-id",
        type=int,
        help="The ID of a specific article to post (defaults to latest)"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force posting even if the article has already been posted"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not actually post to Telegram, just print the message"
    )
    
    return parser.parse_args()

def get_credentials(args):
    """
    Get credentials from command-line arguments or environment variables
    """
    devto_api_key = args.devto_api_key or os.environ.get("DEVTO_API_KEY")
    telegram_bot_token = args.telegram_bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = args.telegram_chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    
    if not all([devto_api_key, telegram_bot_token, telegram_chat_id]):
        print("Error: Missing required credentials.")
        print("Provide them as command-line arguments or environment variables.")
        sys.exit(1)
    
    return devto_api_key, telegram_bot_token, telegram_chat_id

def get_last_posted_article_id():
    """
    Read the ID of the last posted article from the file
    """
    file_path = Path(__file__).parents[1] / "last_posted_article_id.txt"
    
    if not file_path.exists():
        return None
    
    with open(file_path, "r") as file:
        last_id = file.read().strip()
        if last_id.isdigit():
            return int(last_id)
    
    return None

def update_last_posted_article_id(article_id):
    """
    Update the ID of the last posted article in the file
    """
    file_path = Path(__file__).parents[1] / "last_posted_article_id.txt"
    
    with open(file_path, "w") as file:
        file.write(str(article_id))

def main():
    args = setup_argparse()
    devto_api_key, telegram_bot_token, telegram_chat_id = get_credentials(args)
    
    # Initialize clients
    dev_to_client = DevToClient(devto_api_key)
    telegram_client = TelegramMessenger(telegram_bot_token, telegram_chat_id)
    
    # Get the article to post
    try:
        if args.article_id:
            article = dev_to_client.get_article_by_id(args.article_id)
        else:
            article = dev_to_client.get_latest_article()
    except Exception as e:
        print(f"Error fetching article: {e}")
        sys.exit(1)
    
    if not article:
        print("No article found.")
        sys.exit(0)
    
    # Check if the article has already been posted
    last_posted_id = get_last_posted_article_id()
    article_id = article["id"]
    
    if not args.force and last_posted_id is not None and article_id == last_posted_id:
        print(f"Article {article_id} has already been posted. Use --force to post anyway.")
        sys.exit(0)
    
    # Format message
    message = f'New DEV.to article: ["{article["title"]}"]({article["url"]})'
    
    # Post the message
    if args.dry_run:
        print("Dry run mode. Message that would be sent:")
        print(message)
    else:
        try:
            response = telegram_client.send_message(message)
            if response.get("ok"):
                print(f"Message sent to Telegram: {message}")
                # Update the last posted article ID
                update_last_posted_article_id(article_id)
            else:
                print(f"Error from Telegram API: {response}")
                sys.exit(1)
        except Exception as e:
            print(f"Error sending message to Telegram: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
