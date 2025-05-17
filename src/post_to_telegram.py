"""
Script to fetch DEV.to articles and post new ones to Telegram.
"""

import os
import json
import requests
import sys
from pathlib import Path

def get_latest_devto_article(api_key):
    """
    Fetch the latest published article from DEV.to
    """
    headers = {
        "api-key": api_key
    }
    
    url = "https://dev.to/api/articles/me/published"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching articles from DEV.to: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    articles = response.json()
    
    if not articles:
        print("No articles found.")
        return None
    
    # Sort articles by publish date (newest first)
    articles.sort(key=lambda x: x["published_at"], reverse=True)
    return articles[0]

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

def send_telegram_message(bot_token, chat_id, message):
    """
    Send a message to Telegram
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print(f"Error sending message to Telegram: {response.status_code}")
        print(response.text)
        return False
    
    return True

def main():
    # Get environment variables
    devto_api_key = os.environ.get("DEVTO_API_KEY")
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    # Check if all required environment variables are set
    if not all([devto_api_key, telegram_bot_token, telegram_chat_id]):
        print("Error: Missing required environment variables.")
        print("Required variables: DEVTO_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        sys.exit(1)
    
    # Get the latest article from DEV.to
    latest_article = get_latest_devto_article(devto_api_key)
    
    if not latest_article:
        print("No articles found.")
        sys.exit(0)
    
    # Get the ID of the last posted article
    last_posted_id = get_last_posted_article_id()
    
    # Check if the latest article is new
    latest_id = latest_article["id"]
    
    if last_posted_id is None or latest_id != last_posted_id:
        # Format message
        article_title = latest_article["title"]
        article_url = latest_article["url"]
        message = f'New DEV.to article published: ["{article_title}"]({article_url})'
        
        # Send message to Telegram
        sent = send_telegram_message(telegram_bot_token, telegram_chat_id, message)
        
        if sent:
            print(f"Message sent to Telegram: {message}")
            # Update the last posted article ID
            update_last_posted_article_id(latest_id)
        else:
            print("Failed to send message to Telegram.")
    else:
        print("No new articles found.")

if __name__ == "__main__":
    main()
