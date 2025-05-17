# Setting Up a Telegram Bot

To use this project, you need to create a Telegram bot and get its token. Here's how to do that:

## Creating a Bot

1. **Start a conversation with BotFather**:
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Start a chat with BotFather

2. **Create a new bot**:
   - Send the command `/newbot` to BotFather
   - Follow the instructions to set a name and username for your bot
   - The name is what users will see (e.g., "DEV.to Articles Bot")
   - The username must end with "bot" (e.g., "devto_articles_bot")

3. **Get your bot token**:
   - After creating the bot, BotFather will give you a token
   - It looks something like `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`
   - **Keep this token secret!** Anyone with this token can control your bot

## Setting Up Your Bot

1. **Start your bot**:
   - Click on the link that BotFather gives you or search for your bot's username
   - Start a chat with your bot by clicking "Start"

2. **Create a channel or group**:
   - Create a new channel or group where you want to post articles
   - Add your bot as an administrator to the channel/group
   - Make sure to give the bot permission to post messages

3. **Get the chat ID**:
   - For a channel: Forward a message from your channel to [@userinfobot](https://t.me/userinfobot)
   - For a group: Add [@userinfobot](https://t.me/userinfobot) to your group, then check the information it provides
   - The chat ID for a channel looks like: `-1001234567890`
   - The chat ID for a group looks like: `-123456789`

## Configuring the Project

1. **Set up environment variables**:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from BotFather
   - `TELEGRAM_CHAT_ID`: The chat ID of your channel or group

2. **Test your configuration**:
   - Run the `validate_setup.py` script to verify that your bot can post to the channel:

     ```bash
     python tools/validate_setup.py
     ```

## Bot Management Tips

- **Privacy Mode**: By default, bots can only see messages that are explicitly addressed to them. This is fine for this project since we only need to send messages, not read them.

- **Bot Commands**: If you want to add commands to your bot, you can do so by sending `/setcommands` to BotFather.

- **Bot Description**: Set a description for your bot with `/setdescription` in BotFather.

- **Bot Profile Picture**: Set a profile picture with `/setuserpic` in BotFather.

## Troubleshooting

- **Bot isn't sending messages**: Make sure the bot is an administrator in the channel/group with permission to post messages.

- **Wrong chat ID**: Double-check the chat ID format. Channel IDs usually start with `-100`.

- **Bot token is invalid**: Verify that you copied the entire token correctly.

- **Rate limiting**: Telegram has rate limits. If you're sending too many messages too quickly, you might hit these limits. The batch posting tool includes delays between messages to avoid this.
