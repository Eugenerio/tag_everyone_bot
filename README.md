# Telegram Tag Everyone Bot

A simple Telegram bot that tags all members in a chat when the `/tag_all` command is used.

## Features

- Tags all members in a group chat using the `/tag_all` command
- Skips bot accounts when tagging
- Uses HTML formatting for clean mentions
- Error handling for permission issues

## Setup

1. Create a new bot using [@BotFather](https://t.me/BotFather) on Telegram
2. Get your bot token from BotFather
3. Create a `.env` file in the project root with your bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Add the bot to your group chat
2. Make the bot an administrator of the group
3. Use the `/tag_all` command to tag everyone in the chat

## Requirements

- Python 3.7+
- python-telegram-bot
- python-dotenv

## Note

The bot needs to be an administrator in the group to access the member list. Make sure to grant the necessary permissions when adding the bot to a group. 