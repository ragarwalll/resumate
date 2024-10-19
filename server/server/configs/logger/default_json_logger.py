"""This module contains the default logger configuration for the application."""

import os
import re
import logging
from datetime import datetime
import json
from pygments import highlight
from pygments.lexers import JsonLexer  # pylint: disable=no-name-in-module
from pygments.formatters import TerminalFormatter  # pylint: disable=no-name-in-module

from flask import Config
from server.constants import CONFIG_LOG_LEVEL, ENV_LOG_PRETTY

__all__ = ["set_default_logger"]


class ConfigurableColoredJsonFormatter(logging.Formatter):
    """Configurable colored JSON formatter for the application logger."""

    def __init__(
        self,
        fmt=None,
        datefmt=None,
        style="%",
        validate=True,
        *,
        defaults=None,
        pretty_print=False,
    ):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        self.pretty_print = pretty_print

    def strip_ansi(self, text):
        """Remove ANSI escape codes from the text."""
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", text)

    def json_serializer(self, obj, **kwargs):
        """Serialize a JSON object."""
        if self.pretty_print:
            return json.dumps(obj, indent=2, **kwargs)
        return json.dumps(obj, **kwargs)

    def colorize_json(self, json_str, level):
        """Add color to a JSON string if pretty print is enabled."""
        if not self.pretty_print:
            return json_str

        colored_json = highlight(json_str, JsonLexer(), TerminalFormatter())
        colored_level = highlight(
            level.upper(), JsonLexer(), TerminalFormatter()
        ).strip()

        # Add 2 spaces to the colored_json at beginning of each line
        colored_json = colored_json.replace("\n", "\n  ")

        return f"[{colored_level}]: {colored_json}"

    def formatException(self, ei):
        result = super().formatException(ei)
        json_result = {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3],
            "level": "error",
            "logger": "app",
            "msg": self.strip_ansi(result),
            "process_id": os.getpid(),
        }
        json_str = self.json_serializer(json_result)
        return self.colorize_json(json_str, "error")

    def format(self, record):
        record.levelname = record.levelname.lower()
        record.asctime = self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ")[:-3]
        record.process_id = os.getpid()

        log_data = {
            "level": record.levelname,
            "timestamp": record.asctime,
            "logger": record.module,
            "process_id": record.process_id,
            "msg": self.strip_ansi(record.getMessage()),
        }

        json_str = self.json_serializer(log_data)
        return self.colorize_json(json_str, record.levelname)


def set_default_logger(config: Config):
    """Set the configurable logger for the application."""
    # Set log level
    level = config.get(CONFIG_LOG_LEVEL, "INFO").upper()
    log_level = getattr(logging, level)

    # Get pretty print setting
    pretty_print = config.get(ENV_LOG_PRETTY, "false").lower() == "true"

    # Configure root logger
    logging.root.setLevel(log_level)

    # Remove existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Add new handler with our formatter
    json_handler = logging.StreamHandler()
    json_formatter = ConfigurableColoredJsonFormatter(pretty_print=pretty_print)
    json_handler.setFormatter(json_formatter)
    logging.root.addHandler(json_handler)
