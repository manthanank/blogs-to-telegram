"""
Utility functions for interacting with the Telegram API.
"""

import requests
import json

class TelegramMessenger:
    def __init__(self, bot_token, chat_id):
        """
        Initialize the TelegramMessenger with the bot token and chat ID.
        
        Args:
            bot_token (str): The Telegram bot token
            chat_id (str): The Telegram chat ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, text, parse_mode="Markdown"):
        """
        Send a text message to the chat.
        
        Args:
            text (str): The message text
            parse_mode (str): The parsing mode ("Markdown" or "HTML")
        
        Returns:
            dict: The response from the Telegram API
        """
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def send_photo(self, photo_url, caption=None):
        """
        Send a photo to the chat.
        
        Args:
            photo_url (str): The URL of the photo
            caption (str, optional): The caption for the photo
        
        Returns:
            dict: The response from the Telegram API
        """
        url = f"{self.base_url}/sendPhoto"
        payload = {
            "chat_id": self.chat_id,
            "photo": photo_url
        }
        
        if caption:
            payload["caption"] = caption
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def send_document(self, document_url, caption=None):
        """
        Send a document to the chat.
        
        Args:
            document_url (str): The URL of the document
            caption (str, optional): The caption for the document
        
        Returns:
            dict: The response from the Telegram API
        """
        url = f"{self.base_url}/sendDocument"
        payload = {
            "chat_id": self.chat_id,
            "document": document_url
        }
        
        if caption:
            payload["caption"] = caption
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def get_chat_info(self):
        """
        Get information about the chat.
        
        Returns:
            dict: The response from the Telegram API
        """
        url = f"{self.base_url}/getChat"
        payload = {
            "chat_id": self.chat_id
        }
        
        response = requests.post(url, json=payload)
        return response.json()
