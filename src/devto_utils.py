"""
Utility functions for interacting with the DEV.to API.
"""

import requests
import json
from typing import List, Dict, Any, Optional

class DevToClient:
    def __init__(self, api_key: str):
        """
        Initialize the DEV.to API client.
        
        Args:
            api_key (str): Your DEV.to API key
        """
        self.api_key = api_key
        self.base_url = "https://dev.to/api"
        self.headers = {
            "api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def get_my_articles(self, status: str = "published") -> List[Dict[str, Any]]:
        """
        Get a list of your articles.
        
        Args:
            status (str): The status of the articles to fetch
                          ("published", "unpublished", or "all")
        
        Returns:
            List[Dict[str, Any]]: A list of article objects
        """
        valid_statuses = ["published", "unpublished", "all"]
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        
        url = f"{self.base_url}/articles/me/{status}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching articles: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_latest_article(self, status: str = "published") -> Optional[Dict[str, Any]]:
        """
        Get the latest article.
        
        Args:
            status (str): The status of the articles to fetch
                          ("published", "unpublished", or "all")
        
        Returns:
            Optional[Dict[str, Any]]: The latest article object or None if no articles
        """
        articles = self.get_my_articles(status)
        
        if not articles:
            return None
        
        # Sort by published date (newest first)
        articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)
        return articles[0]
    
    def get_article_by_id(self, article_id: int) -> Dict[str, Any]:
        """
        Get an article by its ID.
        
        Args:
            article_id (int): The ID of the article
        
        Returns:
            Dict[str, Any]: The article object
        """
        url = f"{self.base_url}/articles/{article_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching article: {response.status_code} - {response.text}")
        
        return response.json()
    
    def create_article(self, title: str, body_markdown: str, tags: List[str] = None, 
                       publish: bool = False) -> Dict[str, Any]:
        """
        Create a new article.
        
        Args:
            title (str): The title of the article
            body_markdown (str): The body of the article in Markdown
            tags (List[str], optional): A list of tags for the article
            publish (bool, optional): Whether to publish the article
        
        Returns:
            Dict[str, Any]: The created article object
        """
        url = f"{self.base_url}/articles"
        payload = {
            "article": {
                "title": title,
                "body_markdown": body_markdown,
                "published": publish
            }
        }
        
        if tags:
            payload["article"]["tags"] = tags
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code != 201:
            raise Exception(f"Error creating article: {response.status_code} - {response.text}")
        
        return response.json()
