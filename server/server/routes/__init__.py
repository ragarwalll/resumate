"""Route collection"""

__all__ = ["health_ns", "process_ns"]

from .health.route import health_ns
from .process.route import process_ns
