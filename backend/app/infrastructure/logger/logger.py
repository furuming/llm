import logging
from datetime import datetime
from pathlib import Path

from app.shared.config import Settings

LOG_DIRECTORY = Path("/storage/logs")
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(settings: Settings, name: str = "app") -> logging.Logger:
    """アプリケーション共通のファイル logger を返す。"""
    level_name = settings.LOG_LEVEL.upper()
    level = logging.getLevelNamesMapping().get(level_name)
    if level is None:
        msg = f"Invalid LOG_LEVEL: {settings.LOG_LEVEL}"
        raise ValueError(msg)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    log_file = LOG_DIRECTORY / f"{datetime.now():%Y_%m_%d}_app.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # 同じ logger を再取得した場合のログ重複を防ぐ。
    for handler in logger.handlers:
        if (
            isinstance(handler, logging.FileHandler)
            and Path(handler.baseFilename) == log_file
        ):
            handler.setLevel(level)
            return logger

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(handler)

    return logger


logger = get_logger(Settings())
