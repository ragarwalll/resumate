"""Abstract class for pdf to text"""

from abc import ABC, abstractmethod

__all__ = ["PdfToTextParser"]


class PdfToTextParser(ABC):  # pylint: disable=too-few-public-methods
    """Abstract base class for PDF to text parsers."""

    def parse(self, file_path: str) -> str:
        """Public method — calls internal read method"""
        content = self._read_file(file_path)
        return self._process(content)

    @abstractmethod
    def _read_file(self, file_path: str) -> str:
        """To be implemented by subclass for reading"""

    def _process(self, content: str) -> str:
        """Optional hook to process content — can be overridden"""
        return content
