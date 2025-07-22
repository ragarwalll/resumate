# pylint: disable=cyclic-import
"""Extract text from pdf using pymupdf"""

import fitz
from server.services.pdf_to_text.abstract_pdf_to_text import PdfToTextParser

__all__ = ["PDFMinerParser"]


class PDFMinerParser(PdfToTextParser):  # pylint: disable=too-few-public-methods
    """Extract text from pdf using pymupdf"""

    def _read_file(self, file_path: str) -> str:
        doc = fitz.open(file_path)
        return "".join(page.get_text() for page in doc)

    def _process(self, content: str) -> str:
        return content.strip()
