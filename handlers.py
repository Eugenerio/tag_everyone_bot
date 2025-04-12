import logging
from typing import Dict
import time
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import BadRequest

from config import Config

logger = logging.getLogger(__name__)

last_usage: Dict[int, float] = {}

async def check_rate_limit(chat_id: int, rate_limit: int) -> bool:
    """Check if the command is being used too frequently."""
    current_time = time.time()
    if chat_id in last_usage:
        time_passed = current_time - last_usage[chat_id]
        if time_passed < rate_limit:
            return False
    last_usage[chat_id] = current_time
    return True

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    config = context.bot_data.get('config')
    await update.message.reply_text(config.start_message)

async def tag_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /tag_all command."""
    try:
        config = context.bot_data.get('config')
        chat_id = update.effective_chat.id
        logger.info(f"Received tag_all command in chat {chat_id}")
        
        chat = await context.bot.get_chat(chat_id)
        if chat.type == 'private':
            await update.message.reply_text(config.private_chat_message)
            return
            
        if not await check_rate_limit(chat_id, config.rate_limit):
            remaining_time = config.rate_limit - int(time.time() - last_usage[chat_id])
            await update.message.reply_text(
                f"Please wait {remaining_time} seconds before using this command again."
            )
            return
            
        members_count = await context.bot.get_chat_member_count(chat_id)
        logger.info(f"Chat has {members_count} members")
        
        admins = await context.bot.get_chat_administrators(chat_id)
        logger.info(f"Found {len(admins)} administrators")
        
        mentions = []
        for admin in admins:
            if not admin.user.is_bot:
                user = admin.user
                mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions.append(mention)
                logger.info(f"Added mention for user {user.first_name} (ID: {user.id})")
        
        if not mentions:
            await update.message.reply_text(
                config.no_members_message,
                parse_mode=ParseMode.HTML
            )
            return
            
        message = f"{config.attention_message}\n" + ' '.join(mentions)
        await update.message.reply_text(
            text=message,
            parse_mode=ParseMode.HTML
        )
        logger.info("Successfully sent tag message")
        
    except Exception as e:
        logger.error(f"Error in tag_all command: {str(e)}", exc_info=True)
        error_message = config.error_message.format(str(e))
        if "not enough rights" in str(e).lower():
            error_message = config.permission_error_message
        await update.message.reply_text(error_message)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the dispatcher."""
    config = context.bot_data.get('config')
    logger.error("Exception while handling an update:", exc_info=context.error)
    
    error_msg = None
    if isinstance(context.error, BadRequest):
        error_msg = str(context.error)
    else:
        error_msg = f"An unexpected error occurred: {context.error}"
    
    if update and hasattr(update, 'effective_message') and update.effective_message:
        await update.effective_message.reply_text(error_msg) 