"""
Advanced implementation of the DEV.to to Telegram posting workflow.
This script includes:
- Improved error handling
- Logging
- Template-based message formatting
- Retries for API failures
- Metrics collection
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add the project root to the path
sys.path.append(str(Path(__file__).parents[1]))

# Import utility modules
from src.env_loader import load_env
from src.devto_utils import DevToClient
from src.telegram_utils import TelegramMessenger
from src.message_formatter import format_message
from src.logging_utils import setup_logger, log_execution_time

# Set up logger
logger = setup_logger("advanced_poster", to_console=True, to_file=True)

def load_config():
    """
    Load configuration from the config.json file
    """
    config_path = Path(__file__).parents[1] / "config.json"
    
    if not config_path.exists():
        logger.warning("config.json not found. Using default configuration.")
        return {
            "check_interval_hours": 1,
            "telegram_parse_mode": "Markdown",
            "default_template": "default",
            "format_options": {
                "include_cover_image": True,
                "include_tags": True,
                "include_reading_time": True
            },
            "error_notification": {
                "enabled": True,
                "max_retries": 3,
                "retry_delay_seconds": 60
            }
        }
    
    try:
        with open(config_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading config.json: {e}")
        sys.exit(1)

def get_last_posted_article_id():
    """
    Read the ID of the last posted article from the file
    """
    file_path = Path(__file__).parents[1] / "last_posted_article_id.txt"
    
    if not file_path.exists():
        logger.info("last_posted_article_id.txt not found. No previous articles posted.")
        return None
    
    try:
        with open(file_path, "r") as file:
            last_id = file.read().strip()
            if last_id.isdigit():
                return int(last_id)
            else:
                logger.warning(f"Invalid ID in last_posted_article_id.txt: {last_id}")
                return None
    except Exception as e:
        logger.error(f"Error reading last_posted_article_id.txt: {e}")
        return None

def update_last_posted_article_id(article_id):
    """
    Update the ID of the last posted article in the file
    """
    file_path = Path(__file__).parents[1] / "last_posted_article_id.txt"
    
    try:
        with open(file_path, "w") as file:
            file.write(str(article_id))
        logger.info(f"Updated last posted article ID to {article_id}")
    except Exception as e:
        logger.error(f"Error updating last_posted_article_id.txt: {e}")

def update_metrics(metrics):
    """
    Update metrics file with the latest run information
    """
    metrics_path = Path(__file__).parents[1] / "metrics.json"
    
    try:
        existing_metrics = {}
        if metrics_path.exists():
            with open(metrics_path, "r") as file:
                existing_metrics = json.load(file)
        
        # Update metrics
        for key, value in metrics.items():
            existing_metrics[key] = value
        
        # Add timestamp
        existing_metrics["last_update"] = datetime.now().isoformat()
        
        # Write updated metrics
        with open(metrics_path, "w") as file:
            json.dump(existing_metrics, file, indent=2)
        
        logger.debug("Updated metrics file")
    except Exception as e:
        logger.warning(f"Error updating metrics file: {e}")

@log_execution_time(logger, "fetch_and_post")
def fetch_and_post():
    """
    Main function to fetch DEV.to articles and post new ones to Telegram
    """
    # Load configuration
    config = load_config()
    
    # Initialize metrics
    metrics = {
        "last_check": datetime.now().isoformat(),
        "new_articles_found": 0,
        "articles_posted": 0,
        "errors": 0
    }
    
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
        metrics["errors"] += 1
        update_metrics(metrics)
        sys.exit(1)
    
    # Initialize clients
    dev_to_client = DevToClient(devto_api_key)
    telegram_client = TelegramMessenger(telegram_bot_token, telegram_chat_id)
    
    # Get the latest article from DEV.to
    try:
        latest_article = dev_to_client.get_latest_article()
        if not latest_article:
            logger.info("No articles found on DEV.to.")
            update_metrics(metrics)
            return
    except Exception as e:
        logger.error(f"Error fetching latest article from DEV.to: {e}")
        metrics["errors"] += 1
        update_metrics(metrics)
        return
    
    # Get the ID of the last posted article
    last_posted_id = get_last_posted_article_id()
    
    # Check if the latest article is new
    latest_id = latest_article["id"]
    
    if last_posted_id is None or latest_id != last_posted_id:
        metrics["new_articles_found"] += 1
        logger.info(f"New article found: {latest_article['title']} (ID: {latest_id})")
        
        # Format message
        template_name = config.get("default_template", "default")
        message = format_message(latest_article, template_name)
        
        # Send message to Telegram
        error_config = config.get("error_notification", {})
        max_retries = error_config.get("max_retries", 3)
        retry_delay = error_config.get("retry_delay_seconds", 60)
        
        success = False
        
        for attempt in range(max_retries):
            try:
                response = telegram_client.send_message(
                    message, 
                    parse_mode=config.get("telegram_parse_mode", "Markdown")
                )
                
                if response.get("ok"):
                    logger.info(f"Message sent to Telegram: {latest_article['title']}")
                    # Update the last posted article ID
                    update_last_posted_article_id(latest_id)
                    success = True
                    metrics["articles_posted"] += 1
                    break
                else:
                    error_msg = response.get("description", "Unknown error")
                    logger.error(f"Error from Telegram API: {error_msg}")
                    if attempt < max_retries - 1:
                        logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                    metrics["errors"] += 1
            except Exception as e:
                logger.error(f"Error sending message to Telegram: {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                metrics["errors"] += 1
        
        if not success:
            logger.error(f"Failed to send message to Telegram after {max_retries} attempts.")
    else:
        logger.info(f"No new articles found. Last posted article ID: {last_posted_id}")
    
    # Update metrics
    update_metrics(metrics)

def main():
    logger.info("Starting advanced DEV.to to Telegram poster")
    fetch_and_post()
    logger.info("Advanced poster completed")

if __name__ == "__main__":
    main()
