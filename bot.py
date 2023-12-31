import logging

from telegram import Update
from telegram.ext import (
    Application,
)

from config import Config
from kit import load_kits
from ui.handler import ConversationHandlerManager

logger = logging.getLogger("bot")


def main() -> None:
    config = Config("bot.ini")

    logging.basicConfig(
        format=config.log_format, level=logging.getLevelName(config.log_level)
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger.info("Logging is configured")

    logger.info("Loading kits ...")
    load_kits()
    logger.info("Kits are loaded")

    app: Application = Application.builder().token(config.token).build()
    app.add_handler(ConversationHandlerManager.create_handler())

    logger.info("Starting bot ...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
