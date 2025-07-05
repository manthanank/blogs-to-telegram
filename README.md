# Blogs To Telegram

This GitHub Actions workflow automatically posts new articles from your DEV.to account to a specified Telegram chat. The workflow runs every hour and checks for new articles. If a new article is found, it sends a message to the Telegram chat with the article's title and URL.

## Setup

1. **Fork the repository**: Fork this repository to your own GitHub account.

2. **Add Secrets**: Add the following secrets to your GitHub repository:
   - `DEVTO_API_KEY`: Your DEV.to API key.
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
   - `TELEGRAM_CHAT_ID`: The chat ID where you want to post the messages.

3. **Configure the Workflow**: The workflow is defined in `.github/workflows/post-to-telegram.yml`. It is scheduled to run every hour but can also be triggered manually.

## How It Works

1. **Fetch DEV.to Articles**: The workflow fetches the latest published articles from your DEV.to account using the DEV.to API.

2. **Check for New Articles**: It compares the ID of the latest article with the ID stored in `last_posted_article_id.txt`. If they are different, it means a new article has been posted.

3. **Post to Telegram**: If a new article is found, the workflow sends a message to the specified Telegram chat with the article's title and URL.

4. **Update Last Posted Article ID**: The workflow updates the `last_posted_article_id.txt` file in the repository to keep track of the last posted article.

## Running the Workflow

The workflow runs automatically every hour. You can also trigger it manually from the Actions tab in your GitHub repository.

## Example

Here is an example of the message that will be posted to Telegram:

New DEV.to article published: ["How to Automate Your Workflow with GitHub Actions"](https://dev.to/yourusername/how-to-automate-your-workflow-with-github-actions)

## Contributing

Feel free to contribute to this project and help make it better. You can create a pull request with your changes or open an issue if you have any questions or suggestions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Important Note About Workflow Behavior

- The workflow only checks the **latest** published article on DEV.to.
- It will post to Telegram **only if the latest article is new** (i.e., its ID is greater than the one stored in `last_posted_article_id.txt`).
- **Limitation:** If you publish multiple articles between workflow runs, only the most recent (latest) article will be posted to Telegram. Older articles may be skipped.

## Troubleshooting

If your article is not posted to Telegram:

- Make sure your GitHub repository secrets are set correctly:
  - `DEVTO_API_KEY` (your DEV.to API key)
  - `TELEGRAM_BOT_TOKEN` (your Telegram bot token)
  - `TELEGRAM_CHAT_ID` (the chat/channel ID for posting)
- Check the Actions tab for workflow run logs and errors.
- Ensure your Telegram bot is in the target chat and has permission to post.
- Confirm that your latest article's ID is greater than the one in `last_posted_article_id.txt`.
