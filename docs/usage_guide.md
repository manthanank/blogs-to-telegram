# Usage Guide

This guide explains how to use the Blogs to Telegram project for different scenarios.

## Basic Usage

### Automatic Posting with GitHub Actions

The project is designed to run automatically using GitHub Actions. Once set up, it will check for new articles every hour and post them to your Telegram chat.

1. **Fork the repository** to your GitHub account
2. **Set up secrets** in your GitHub repository:
   - `DEVTO_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. **Enable GitHub Actions** in your repository

That's it! The workflow will run automatically according to the schedule.

### Manual Triggering

You can also trigger the workflow manually:

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Post DEV.to Articles to Telegram" workflow
3. Click "Run workflow"
4. Click "Run workflow" again in the popup

## Local Usage

### Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your credentials (see [LOCAL_DEVELOPMENT.md](../LOCAL_DEVELOPMENT.md))

### Validating Your Setup

Before posting articles, it's a good idea to validate your setup:

```bash
python tools/validate_setup.py
```

This will check:

- Environment variables
- Configuration file
- Connectivity to DEV.to API
- Connectivity to Telegram API

### Posting the Latest Article

To post your latest DEV.to article to Telegram:

```bash
python src/post_to_telegram.py
```

Or use the enhanced version:

```bash
python src/enhanced_post_to_telegram.py
```

Or the advanced version:

```bash
python src/advanced_post_to_telegram.py
```

### Manual Posting

To manually post a specific article:

```bash
python tools/manual_post.py --article-id 123456
```

Options:

- `--article-id ID`: Post a specific article by ID
- `--force`: Post even if the article has already been posted
- `--dry-run`: Don't actually post, just show what would be posted

### Batch Posting

```bash
To post multiple articles at once (useful for initially populating a channel):

```bash
python tools/batch_post.py --count 10
```

Options:

- `--count N`: Post N articles (default: 5)
- `--delay N`: Wait N seconds between posts (default: 3)
- `--template NAME`: Use a specific template (default: default)
- `--reverse`: Post oldest articles first
- `--dry-run`: Don't actually post, just show what would be posted

## Customizing Messages

### Templates

The project uses templates to format messages. Templates are stored in the `templates` directory as JSON files.

Two templates are included:

- `default.json`: A rich template with title, description, tags, etc.
- `compact.json`: A minimal template with just the title and URL

To use a different template:

```bash
python tools/batch_post.py --template compact
```

### Creating Custom Templates

You can create your own templates:

1. Create a new JSON file in the `templates` directory
2. Include the following fields:
   - `name`: A name for your template
   - `template`: The template string
   - `description`: (optional) A description of the template

Template variables:

- `{{title}}`: The article title
- `{{url}}`: The article URL
- `{{description}}`: The article description
- `{{published_at}}`: The publication timestamp
- `{{published_date}}`: The formatted publication date
- `{{published_time}}`: The formatted publication time
- `{{tags}}`: The article tags (formatted as hashtags)
- `{{reading_time}}`: The reading time in minutes
- `{{user}}`: The author's name
- `{{username}}`: The author's username
- `{{cover_image}}`: The cover image URL

Conditional blocks:

- `{{#if variable}}content{{/if}}`: Include content only if variable exists

Example template:

```json
{
  "name": "My Custom Template",
  "template": "📢 New Article: {{title}}\n\n{{#if description}}{{description}}{{/if}}\n\n🔗 {{url}}",
  "description": "A custom template with emoji"
}
```

## Configuration

The `config.json` file in the root directory allows you to customize the project's behavior:

```json
{
  "message_template": "New DEV.to article published: [\"{title}\"]({url})",
  "check_interval_hours": 1,
  "telegram_parse_mode": "Markdown",
  "format_options": {
    "include_cover_image": true,
    "include_tags": true,
    "include_reading_time": true
  },
  "error_notification": {
    "enabled": true,
    "max_retries": 3,
    "retry_delay_seconds": 60
  }
}
```

Key settings:

- `telegram_parse_mode`: Parsing mode for Telegram messages ("Markdown" or "HTML")
- `default_template`: The default template to use
- `error_notification.max_retries`: Number of retries on failure
- `error_notification.retry_delay_seconds`: Seconds to wait between retries

## Logs and Monitoring

### Logs

Logs are stored in the `logs` directory. The advanced script creates detailed logs that can help with troubleshooting.

### Metrics

The advanced script also collects metrics in `metrics.json`, which include:

- Last check time
- Number of new articles found
- Number of articles posted
- Number of errors
