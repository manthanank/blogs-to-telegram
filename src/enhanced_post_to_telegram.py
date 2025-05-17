"""
Enhanced script to fetch DEV.to articles and post new ones to Telegram.
This version uses the utility classes and the configuration file.
"""

import os
import json
import sys
from pathlib import Path
import time
from datetime import datetime

# Import utility modules
from devto_utils import DevToClient
from telegram_utils import TelegramMessenger

def load_config():
    """
    Load configuration from the config.json file
    """
    config_path = Path(__file__).parents[1] / "config.json"
    
    if not config_path.exists():
        print("Warning: config.json not found. Using default configuration.")
        return {
            "message_template": "New DEV.to article published: [\"{title}\"]({url})",
            "check_interval_hours": 1,
            "telegram_parse_mode": "Markdown",
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
    
    with open(config_path, "r") as file:
        return json.load(file)

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

def format_message(article, config):
    """
    Format the message to be sent to Telegram using the template and options from config
    """
    message = config["message_template"].format(
        title=article["title"],
        url=article["url"]
    )
    
    # Add additional information based on format options
    format_options = config.get("format_options", {})
    
    if format_options.get("include_tags", False) and article.get("tag_list"):
        tags = " ".join([f"#{tag.replace(' ', '')}" for tag in article["tag_list"]])
        message += f"\n\nTags: {tags}"
    
    if format_options.get("include_reading_time", False) and article.get("reading_time_minutes"):
        message += f"\n\nReading time: {article['reading_time_minutes']} min"
    
    return message

def main():
    # Load configuration
    config = load_config()
    
    # Get environment variables
    devto_api_key = os.environ.get("DEVTO_API_KEY")
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    # Check if all required environment variables are set
    if not all([devto_api_key, telegram_bot_token, telegram_chat_id]):
        print("Error: Missing required environment variables.")
        print("Required variables: DEVTO_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        sys.exit(1)
    
    # Initialize clients
    dev_to_client = DevToClient(devto_api_key)
    telegram_client = TelegramMessenger(telegram_bot_token, telegram_chat_id)
    
    # Get the latest article from DEV.to
    try:
        latest_article = dev_to_client.get_latest_article()
    except Exception as e:
        print(f"Error fetching latest article: {e}")
        sys.exit(1)
    
    if not latest_article:
        print("No articles found.")
        sys.exit(0)
    
    # Get the ID of the last posted article
    last_posted_id = get_last_posted_article_id()
    
    # Check if the latest article is new
    latest_id = latest_article["id"]
    
    if last_posted_id is None or latest_id != last_posted_id:
        # Format message
        message = format_message(latest_article, config)
        
        # Send message to Telegram
        error_config = config.get("error_notification", {})
        max_retries = error_config.get("max_retries", 3)
        retry_delay = error_config.get("retry_delay_seconds", 60)
        
        for attempt in range(max_retries):
            try:
                response = telegram_client.send_message(
                    message, 
                    parse_mode=config.get("telegram_parse_mode", "Markdown")
                )
                
                if response.get("ok"):
                    print(f"Message sent to Telegram: {message}")
                    # Update the last posted article ID
                    update_last_posted_article_id(latest_id)
                    break
                else:
                    print(f"Error from Telegram API: {response}")
                    if attempt < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
            except Exception as e:
                print(f"Error sending message to Telegram: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
        else:
            print(f"Failed to send message to Telegram after {max_retries} attempts.")
    else:
        print("No new articles found.")
        
    # Log the check
    print(f"Check completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
