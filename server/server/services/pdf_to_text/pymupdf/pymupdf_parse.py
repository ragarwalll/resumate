"""Extract text from pdf using pymupdf"""

from pdfminer.high_level import extract_text
from server.services.pdf_to_text.abstract_pdf_to_text import PdfToTextParser

__all__ = ["PymupdfParser"]


class PymupdfParser(PdfToTextParser):  # pylint: disable=too-few-public-methods
    """Extract text from pdf using pymupdf"""

    def _read_file(self, file_path: str) -> str:
        return extract_text(file_path)

    def _process(self, content: str) -> str:
        return content.strip()
