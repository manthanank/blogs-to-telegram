# Setting Up DEV.to API Access

To fetch articles from your DEV.to account, you need to create an API key. Here's how to do that:

## Getting an API Key

1. **Log in to DEV.to**:
   - Go to [DEV.to](https://dev.to/) and log in to your account

2. **Go to Settings**:
   - Click on your profile picture in the top-right corner
   - Select "Settings" from the dropdown menu

3. **Go to Account**:
   - In the left sidebar, click on "Account"
   - Scroll down to the "DEV API Keys" section

4. **Create a new API Key**:
   - Enter a description for your key (e.g., "Blogs to Telegram")
   - Click "Generate API Key"
   - Copy the generated API key
   - **Important**: This key will only be shown once! Make sure to copy it immediately.

## Understanding the DEV.to API

The DEV.to API allows you to:

- Fetch your published articles
- Get article details
- Create, update, and delete articles
- and more

For this project, we primarily use the endpoint to fetch your published articles:

```bash
GET https://dev.to/api/articles/me/published
```

### API Response Format

The API returns your articles in JSON format. Here's a simplified example of what the response looks like:

```json
[
  {
    "id": 123456,
    "title": "My Awesome Article",
    "description": "This is a great article about something cool",
    "published_at": "2023-01-15T12:30:45Z",
    "tag_list": ["javascript", "webdev", "tutorial"],
    "url": "https://dev.to/username/my-awesome-article-123",
    "reading_time_minutes": 5,
    "user": {
      "name": "Your Name",
      "username": "yourusername"
    }
  }
]
```

### API Rate Limits

DEV.to has rate limits on their API. According to their documentation:

- 30 requests per 30-second period

This is more than enough for our use case, as we're typically making one request per hour.

## Configuring the Project

1. **Set up environment variables**:
   - `DEVTO_API_KEY`: Your API key from DEV.to

2. **Test your configuration**:
   - Run the `validate_setup.py` script to verify that your API key is working:

     ```bash
     python tools/validate_setup.py
     ```

## Troubleshooting

- **Invalid API key**: Make sure you copied the entire API key correctly.

- **No articles found**: Ensure that you have published articles on your DEV.to account.

- **API changes**: If DEV.to changes their API, you might need to update the project. Check their [API documentation](https://developers.forem.com/api) for the latest information.

- **Rate limiting**: If you're making too many requests, you might hit rate limits. The project includes retry logic to handle this.
