import configparser
import logging

from telegram import Update
from telegram.ext import (
    Application,
)

from ui.handler import (
    conversation_handler,
)


class Config:
    """
    You should configure the bot by creating a bot.ini file:
    ----------------------------------------------------------
    [DEFAULT]
    token=<bot token, required>
    [LOGGING]
    format=<log format, optional, default - %(asctime)s - %(name)s - %(levelname)s - %(message)s>
    level=<log level, optional, default - INFO>
    ----------------------------------------------------------
    """

    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read("bot.ini")
        self.token = parser.get("DEFAULT", "token")
        self.log_format = parser.get(
            "LOGGING",
            "format",
            fallback="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.log_level = parser.get("LOGGING", "level", fallback="INFO")


config = Config()
logging.basicConfig(
    format=config.log_format, level=logging.getLevelName(config.log_level)
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    app: Application = Application.builder().token(config.token).build()
    app.add_handler(conversation_handler)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            "\nConversation states, callbacks, patterns:\n\t"
            + "\n\t".join(
                [
                    f"{key}, {el.callback.__name__}, {el.pattern.pattern}"
                    for key in conversation_handler.states.keys()
                    for el in conversation_handler.states[key]
                ]
            )
        )
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
