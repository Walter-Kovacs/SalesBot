import configparser


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

    def __init__(self, ini_file_path: str) -> None:
        parser = configparser.ConfigParser()
        parser.read(ini_file_path)
        self.token = parser.get("DEFAULT", "token")
        self.log_format = parser.get(
            "LOGGING",
            "format",
            fallback="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.log_level = parser.get("LOGGING", "level", fallback="INFO")
