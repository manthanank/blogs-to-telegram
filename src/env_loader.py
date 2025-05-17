"""
Helper script to load environment variables from a .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """
    Load environment variables from .env file
    """
    env_path = Path(__file__).parents[1] / ".env"
    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print("Loaded environment variables from .env file.")
    else:
        print("No .env file found. Using existing environment variables.")
        
    # Check if required variables are set
    required_vars = ["DEVTO_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {', '.join(missing_vars)}")
        print("Create a .env file based on .env.sample or set these variables in your environment.")
        
    return not missing_vars
