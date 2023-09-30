import configparser
import logging

from telegram import Update
from telegram.ext import (
    Application,
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
        parser.read('bot.ini')
        self.token = parser.get('DEFAULT', 'token')
        self.log_format = \
            parser.get('LOGGING', 'format', fallback='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_level = \
            parser.get('LOGGING', 'level', fallback='INFO')


config = Config()
logging.basicConfig(format=config.log_format, level=logging.getLevelName(config.log_level))
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    app: Application = Application.builder().token(config.token).build()

    # ...

    app.run_polling(
        allowed_updates=[
            Update.CALLBACK_QUERY,
        ]
    )


if __name__ == '__main__':
    main()
