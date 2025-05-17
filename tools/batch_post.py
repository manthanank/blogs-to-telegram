"""
Script to post multiple DEV.to articles to Telegram.
Useful for initially populating a channel with existing articles.
"""

import os
import sys
import argparse
import time
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parents[1]))

from src.env_loader import load_env
from src.devto_utils import DevToClient
from src.telegram_utils import TelegramMessenger
from src.message_formatter import format_message
from src.logging_utils import setup_logger, log_execution_time

# Set up logger
logger = setup_logger("batch_post", to_console=True, to_file=True)

def setup_argparse():
    """
    Set up command-line argument parsing
    """
    parser = argparse.ArgumentParser(
        description="Post multiple DEV.to articles to Telegram"
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="The number of articles to post (default: 5)"
    )
    
    parser.add_argument(
        "--delay",
        type=int,
        default=3,
        help="The delay between posts in seconds (default: 3)"
    )
    
    parser.add_argument(
        "--template",
        default="default",
        help="The name of the template to use (default: default)"
    )
    
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Post articles in reverse order (oldest first)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not actually post to Telegram, just print the messages"
    )
    
    return parser.parse_args()

@log_execution_time(logger, "fetch_articles")
def fetch_articles(dev_to_client, count, reverse=False):
    """
    Fetch articles from DEV.to
    """
    try:
        articles = dev_to_client.get_my_articles()
        
        if not articles:
            logger.warning("No articles found.")
            return []
        
        # Sort articles by publish date
        articles.sort(key=lambda x: x.get("published_at", ""), reverse=not reverse)
        
        # Limit to the requested count
        return articles[:count]
    except Exception as e:
        logger.error(f"Error fetching articles: {e}")
        return []

@log_execution_time(logger, "post_articles")
def post_articles(articles, telegram_client, template_name, delay, dry_run):
    """
    Post articles to Telegram
    """
    total = len(articles)
    success_count = 0
    fail_count = 0
    
    for i, article in enumerate(articles, 1):
        try:
            # Format message
            message = format_message(article, template_name)
            
            # Log
            logger.info(f"[{i}/{total}] Posting article: {article['title']}")
            
            if dry_run:
                logger.info(f"DRY RUN: Message that would be sent:\n{message}")
                success_count += 1
            else:
                # Send message
                response = telegram_client.send_message(message)
                
                if response.get("ok"):
                    logger.info(f"Successfully posted article: {article['id']}")
                    success_count += 1
                else:
                    logger.error(f"Error from Telegram API: {response}")
                    fail_count += 1
            
            # Wait before posting the next article (if not the last one)
            if i < total and delay > 0:
                logger.info(f"Waiting for {delay} seconds before posting the next article...")
                time.sleep(delay)
        except Exception as e:
            logger.error(f"Error posting article {article.get('id')}: {e}")
            fail_count += 1
    
    return success_count, fail_count

def main():
    args = setup_argparse()
    
    # Load environment variables
    load_env()
    
    # Get environment variables
    devto_api_key = os.environ.get("DEVTO_API_KEY")
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    # Check if all required environment variables are set
    if not all([devto_api_key, telegram_bot_token, telegram_chat_id]):
        logger.error("Missing required environment variables.")
        logger.error("Required variables: DEVTO_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        sys.exit(1)
    
    # Initialize clients
    dev_to_client = DevToClient(devto_api_key)
    telegram_client = TelegramMessenger(telegram_bot_token, telegram_chat_id)
    
    # Fetch articles
    logger.info(f"Fetching up to {args.count} articles from DEV.to...")
    articles = fetch_articles(dev_to_client, args.count, args.reverse)
    
    if not articles:
        logger.warning("No articles to post.")
        sys.exit(0)
    
    # Post articles
    logger.info(f"Found {len(articles)} articles to post.")
    logger.info(f"Using template: {args.template}")
    
    if args.dry_run:
        logger.info("DRY RUN MODE: Articles will not actually be posted.")
    
    success_count, fail_count = post_articles(
        articles, 
        telegram_client, 
        args.template, 
        args.delay, 
        args.dry_run
    )
    
    # Log summary
    logger.info(f"Batch posting complete. Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    main()
