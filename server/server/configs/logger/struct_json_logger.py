"""Logging configuration for the application."""

import os
import json
import logging
import structlog
from pygments import highlight
from pygments.lexers import JsonLexer  # pylint: disable=no-name-in-module
from pygments.formatters import TerminalFormatter  # pylint: disable=no-name-in-module

from flask import Config
from server.constants import CONFIG_LOG_LEVEL, ENV_LOG_PRETTY

__all__ = ["configure_logging"]


def set_process_id(_, __, event_dict):
    """Set the process ID in the event dictionary."""

    event_dict["process_id"] = os.getpid()
    return event_dict


def set_logger(_, __, event_dict):
    """Set the logger in the event dictionary."""

    event_dict["logger"] = "app"
    return event_dict


def configure_logging(config: Config):
    """Configure logging for the application."""

    processors = (
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        set_process_id,
        set_logger,
        structlog.processors.EventRenamer("msg"),
    )

    # get the log level from the configuration
    level = config.get(CONFIG_LOG_LEVEL, "INFO").upper()
    log_level = getattr(logging, level)

    # get pretty print is enabled or not
    pretty_print = config.get(ENV_LOG_PRETTY) == "true"

    # if pretty print is enabled, add JSONRenderer with colored_json_serializer
    if pretty_print:
        processors += (
            structlog.processors.JSONRenderer(serializer=colored_json_serializer),
        )
    else:
        processors += (structlog.processors.JSONRenderer(),)

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=processors,
    )


def colored_json_serializer(obj, **kwargs):
    """Serialize a JSON object with color.

    Args:
        obj (dict): The JSON object to serialize.

    Returns:
        str: The serialized JSON object with color.
    """
    level = obj.get("level").upper()

    json_str = json.dumps(obj, indent=2, **kwargs)
    colored_json = highlight(json_str, JsonLexer(), TerminalFormatter())
    colored_level = highlight(level, JsonLexer(), TerminalFormatter())

    # remove new line from colored_level
    colored_level = colored_level.replace("\n", "")

    # add 2 spaces to the colored_json at beginning of each line
    colored_json = colored_json.replace("\n", "\n  ")

    return f"[{colored_level}]: {colored_json}"
