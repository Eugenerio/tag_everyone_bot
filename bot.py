import logging
from telegram.ext import Application, CommandHandler

from config import Config
from handlers import start_command, tag_all_command, error_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    config = Config.load()
    if not config:
        logger.error("No token found! Make sure to set TELEGRAM_BOT_TOKEN environment variable.")
        return

    try:
        application = Application.builder().token(config.token).build()
        
        application.bot_data['config'] = config

        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("tag_all", tag_all_command))
        
        application.add_error_handler(error_handler)

        logger.info("Starting bot...")
        application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True
        )
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)

if __name__ == '__main__':
    main() 