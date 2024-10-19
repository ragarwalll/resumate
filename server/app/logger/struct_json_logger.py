"""Logging configuration for the application."""

import os
import structlog

__all__ = ["configure_logging"]

def set_process_id(_, __, event_dict):
    """Set the process ID in the event dictionary."""

    event_dict["process_id"] = os.getpid()
    return event_dict

def configure_logging():
    """Configure logging for the application."""

    structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        set_process_id,
        structlog.processors.EventRenamer("msg"),
        structlog.processors.JSONRenderer()
        ]
    )
