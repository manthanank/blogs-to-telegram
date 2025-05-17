"""
Message formatting utilities for customizing Telegram messages.
"""

import json
import os
from pathlib import Path
import re
from datetime import datetime

def load_message_templates():
    """
    Load message templates from the templates directory.
    
    Returns:
        dict: A dictionary of template names to template strings
    """
    templates_dir = Path(__file__).parents[1] / "templates"
    
    # Create templates directory if it doesn't exist
    os.makedirs(templates_dir, exist_ok=True)
    
    # If the default template doesn't exist, create it
    default_template_path = templates_dir / "default.json"
    if not default_template_path.exists():
        default_template = {
            "name": "Default Template",
            "template": "New DEV.to article published: [\"{{title}}\"]({{url}})\n\n{{#if tags}}Tags: {{tags}}{{/if}}{{#if reading_time}}\n\nReading time: {{reading_time}} min{{/if}}"
        }
        
        with open(default_template_path, "w") as file:
            json.dump(default_template, file, indent=2)
    
    # Load all templates
    templates = {}
    
    for file_path in templates_dir.glob("*.json"):
        try:
            with open(file_path, "r") as file:
                template_data = json.load(file)
                if "name" in template_data and "template" in template_data:
                    templates[file_path.stem] = template_data
        except Exception as e:
            print(f"Error loading template from {file_path.name}: {e}")
    
    return templates

def format_message(article, template_name="default"):
    """
    Format a message using the specified template.
    
    Args:
        article (dict): The article data from DEV.to
        template_name (str): The name of the template to use
    
    Returns:
        str: The formatted message
    """
    # Load templates
    templates = load_message_templates()
    
    # Get the template
    template_data = templates.get(template_name)
    if not template_data:
        # Fallback to a basic template if the specified one doesn't exist
        return f'New DEV.to article published: ["{article["title"]}"]({article["url"]})'
    
    # Get the template string
    template_str = template_data["template"]
    
    # Prepare data for template
    data = {
        "title": article.get("title", ""),
        "url": article.get("url", ""),
        "description": article.get("description", ""),
        "published_at": article.get("published_at", ""),
        "tags": " ".join([f"#{tag.replace(' ', '')}" for tag in article.get("tag_list", [])]),
        "reading_time": article.get("reading_time_minutes", ""),
        "user": article.get("user", {}).get("name", ""),
        "username": article.get("user", {}).get("username", ""),
        "cover_image": article.get("cover_image", "")
    }
    
    # Format published_at as a readable date if it exists
    if data["published_at"]:
        try:
            dt = datetime.fromisoformat(data["published_at"].replace("Z", "+00:00"))
            data["published_date"] = dt.strftime("%B %d, %Y")
            data["published_time"] = dt.strftime("%I:%M %p")
        except:
            data["published_date"] = ""
            data["published_time"] = ""
    
    # Replace variables in the template
    message = template_str
    
    # Handle simple variable replacements {{var}}
    for key, value in data.items():
        if value is not None and value != "":
            message = message.replace(f"{{{{{key}}}}}", str(value))
    
    # Handle conditional blocks {{#if var}}content{{/if}}
    for key in data:
        if_pattern = f"{{{{#if {key}}}}}(.*?){{{{/if}}}}"
        value = data.get(key)
        
        if value and value != "":
            # If the value exists, replace the conditional block with its content
            message = re.sub(if_pattern, r"\1", message)
        else:
            # If the value doesn't exist or is empty, remove the conditional block
            message = re.sub(if_pattern, "", message)
    
    return message
