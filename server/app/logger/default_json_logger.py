"""This module contains the default logger configuration for the application."""

import os
import logging
from datetime import datetime
import json

__all__ = ["set_default_logger"]

class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for the application logger."""

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        self.process_id = None

    def formatException(self, ei):
        result = super().formatException(ei)
        json_result = {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3],
            "level": "error",
            "logger": "app",
            "msg": f"{result}",
            "process_id":os.getpid()
        }
        return json.dumps(json_result)

    def format(self, record):
        record.levelname = record.levelname.lower()
        record.asctime = self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ")[:-3]

        # Add the test field to the record
        record.process_id = os.getpid()

        return super().format(record)

def set_default_logger():
    """Set the default logger for the application."""

    json_handler = logging.StreamHandler()
    json_formatter = JsonFormatter(
        '{"level": "%(levelname)s", \
        "timestamp": "%(asctime)s", \
        "logger": "%(module)s", \
        "process_id": "%(process_id)s", \
        "msg": "%(message)s"}'
    )
    json_handler.setFormatter(json_formatter)
    logging.root.addHandler(json_handler)
