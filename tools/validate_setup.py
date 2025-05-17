"""
Test script to validate the setup and configuration.
This script checks:
1. Environment variables are correctly set
2. Connectivity to DEV.to API
3. Connectivity to Telegram API
4. Configuration file validity
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parents[1]))

from src.env_loader import load_env
from src.devto_utils import DevToClient
from src.telegram_utils import TelegramMessenger

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("\n--- Checking environment variables ---")
    
    # Load environment variables from .env file if available
    load_env()
    
    # Check required variables
    required_vars = ["DEVTO_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
    all_present = True
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask the value for security
            masked_value = value[:3] + "*" * (len(value) - 6) + value[-3:] if len(value) > 6 else "***"
            print(f"✅ {var} is set: {masked_value}")
        else:
            print(f"❌ {var} is not set")
            all_present = False
    
    return all_present

def check_config_file():
    """Check if the configuration file exists and is valid"""
    print("\n--- Checking configuration file ---")
    
    config_path = Path(__file__).parents[1] / "config.json"
    
    if not config_path.exists():
        print("❌ config.json not found")
        return False
    
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        
        # Check required fields
        required_fields = ["message_template", "telegram_parse_mode"]
        for field in required_fields:
            if field not in config:
                print(f"❌ Required field '{field}' missing in config.json")
                return False
        
        print("✅ config.json exists and is valid")
        return True
    except json.JSONDecodeError:
        print("❌ config.json is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return False

def check_devto_api():
    """Check connectivity to the DEV.to API"""
    print("\n--- Checking DEV.to API connectivity ---")
    
    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        print("❌ Cannot check DEV.to API: API key not set")
        return False
    
    try:
        client = DevToClient(api_key)
        articles = client.get_my_articles()
        
        if articles is not None:
            print(f"✅ Successfully connected to DEV.to API (found {len(articles)} articles)")
            return True
        else:
            print("❌ Failed to get articles from DEV.to API")
            return False
    except Exception as e:
        print(f"❌ Error connecting to DEV.to API: {e}")
        return False

def check_telegram_api():
    """Check connectivity to the Telegram API"""
    print("\n--- Checking Telegram API connectivity ---")
    
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("❌ Cannot check Telegram API: Bot token or chat ID not set")
        return False
    
    try:
        client = TelegramMessenger(bot_token, chat_id)
        info = client.get_chat_info()
        
        if info.get("ok"):
            chat_type = info.get("result", {}).get("type", "unknown")
            chat_title = info.get("result", {}).get("title", "Unknown")
            
            if chat_title:
                print(f"✅ Successfully connected to Telegram API (Chat: {chat_title}, Type: {chat_type})")
            else:
                print(f"✅ Successfully connected to Telegram API (Chat ID: {chat_id})")
            return True
        else:
            print(f"❌ Failed to get chat info from Telegram API: {info.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to Telegram API: {e}")
        return False

def check_last_posted_article():
    """Check if the last posted article file exists and is valid"""
    print("\n--- Checking last posted article file ---")
    
    file_path = Path(__file__).parents[1] / "last_posted_article_id.txt"
    
    if not file_path.exists():
        print("ℹ️ last_posted_article_id.txt not found (will be created on first run)")
        return True
    
    try:
        with open(file_path, "r") as file:
            last_id = file.read().strip()
            
            if last_id.isdigit():
                print(f"✅ last_posted_article_id.txt exists and contains a valid ID: {last_id}")
                return True
            else:
                print(f"❌ last_posted_article_id.txt does not contain a valid ID")
                return False
    except Exception as e:
        print(f"❌ Error reading last_posted_article_id.txt: {e}")
        return False

def run_all_checks():
    """Run all checks and report results"""
    print("🔍 Starting setup validation checks\n")
    
    env_check = check_environment_variables()
    config_check = check_config_file()
    devto_check = check_devto_api() if env_check else False
    telegram_check = check_telegram_api() if env_check else False
    last_article_check = check_last_posted_article()
    
    # Summarize results
    print("\n--- Summary ---")
    print(f"Environment variables: {'✅ PASS' if env_check else '❌ FAIL'}")
    print(f"Configuration file: {'✅ PASS' if config_check else '❌ FAIL'}")
    print(f"DEV.to API connectivity: {'✅ PASS' if devto_check else '❌ FAIL'}")
    print(f"Telegram API connectivity: {'✅ PASS' if telegram_check else '❌ FAIL'}")
    print(f"Last posted article file: {'✅ PASS' if last_article_check else '❌ FAIL'}")
    
    all_checks_passed = env_check and config_check and devto_check and telegram_check and last_article_check
    
    if all_checks_passed:
        print("\n✅ All checks passed! Your setup is complete and working correctly.")
    else:
        print("\n❌ Some checks failed. Please fix the issues above before running the main script.")
    
    return all_checks_passed

if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
