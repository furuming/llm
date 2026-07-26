import logging
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest

from app.infrastructure.logger import logger as logger_module
from app.shared.config import Settings


def _logger_name() -> str:
    return f"test.logger.{uuid4()}"


def _close_handlers(logger: logging.Logger) -> None:
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()


def test_get_logger_writes_to_dated_log_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(logger_module, "LOG_DIRECTORY", tmp_path)
    logger = logger_module.get_logger(Settings(LOG_LEVEL="INFO"), _logger_name())

    try:
        logger.info("application started")
        for handler in logger.handlers:
            handler.flush()

        expected_file = tmp_path / f"{datetime.now():%Y_%m_%d}_app.log"
        assert expected_file.exists()
        assert "INFO" in expected_file.read_text(encoding="utf-8")
        assert "application started" in expected_file.read_text(encoding="utf-8")
    finally:
        _close_handlers(logger)


def test_get_logger_uses_log_level_from_settings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(logger_module, "LOG_DIRECTORY", tmp_path)
    logger = logger_module.get_logger(Settings(LOG_LEVEL="ERROR"), _logger_name())

    try:
        logger.info("not written")
        logger.error("written")
        for handler in logger.handlers:
            handler.flush()

        log_file = next(tmp_path.glob("*_app.log"))
        content = log_file.read_text(encoding="utf-8")
        assert "not written" not in content
        assert "written" in content
    finally:
        _close_handlers(logger)


def test_get_logger_does_not_duplicate_file_handler(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(logger_module, "LOG_DIRECTORY", tmp_path)
    name = _logger_name()
    logger = logger_module.get_logger(Settings(), name)

    try:
        same_logger = logger_module.get_logger(Settings(), name)

        assert same_logger is logger
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.FileHandler)
    finally:
        _close_handlers(logger)


def test_get_logger_raises_value_error_for_invalid_log_level() -> None:
    with pytest.raises(ValueError, match="Invalid LOG_LEVEL: UNKNOWN"):
        logger_module.get_logger(Settings(LOG_LEVEL="UNKNOWN"), _logger_name())


def test_logger_switches_file_when_date_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_datetime = datetime

    class MutableDatetime:
        current = real_datetime(2026, 7, 26, 23, 59, 59)

        @classmethod
        def now(cls) -> datetime:
            return cls.current

    monkeypatch.setattr(logger_module, "LOG_DIRECTORY", tmp_path)
    monkeypatch.setattr(logger_module, "datetime", MutableDatetime)
    logger = logger_module.get_logger(Settings(), _logger_name())

    try:
        logger.info("before midnight")
        MutableDatetime.current = real_datetime(2026, 7, 27, 0, 0, 1)
        logger.info("after midnight")
        for handler in logger.handlers:
            handler.flush()

        previous_file = tmp_path / "2026_07_26_app.log"
        current_file = tmp_path / "2026_07_27_app.log"
        assert "before midnight" in previous_file.read_text(encoding="utf-8")
        assert "after midnight" not in previous_file.read_text(encoding="utf-8")
        assert "after midnight" in current_file.read_text(encoding="utf-8")
    finally:
        _close_handlers(logger)
