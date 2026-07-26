import logging
from datetime import date, datetime
from pathlib import Path

from app.shared.config import Settings

LOG_DIRECTORY = Path("/storage/logs")
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class DailyFileHandler(logging.FileHandler):
    """日付が変わったときに当日分のログファイルへ切り替える。"""

    def __init__(self, directory: Path, encoding: str = "utf-8"):
        self.directory = directory.resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self._current_date = datetime.now().date()
        super().__init__(self._log_file(self._current_date), encoding=encoding)

    def _log_file(self, target_date: date) -> Path:
        return self.directory / f"{target_date:%Y_%m_%d}_app.log"

    def ensure_current_file(self) -> None:
        """必要であれば出力先を当日分のファイルへ切り替える。"""
        today = datetime.now().date()
        if today == self._current_date:
            return

        if self.stream is not None:
            self.stream.flush()
            self.stream.close()
            self.stream = None

        self._current_date = today
        self.baseFilename = str(self._log_file(today).resolve())
        self.stream = self._open()

    def emit(self, record: logging.LogRecord) -> None:
        self.ensure_current_file()
        super().emit(record)


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

    log_directory = LOG_DIRECTORY.resolve()

    # 同じ logger を再取得した場合のログ重複を防ぐ。
    for handler in logger.handlers:
        if (
            isinstance(handler, DailyFileHandler)
            and handler.directory == log_directory
        ):
            handler.ensure_current_file()
            handler.setLevel(level)
            return logger

    handler = DailyFileHandler(log_directory)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(handler)

    return logger


logger = get_logger(Settings())
