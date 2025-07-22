"""PDF to text"""

import structlog
from server.services.pdf_to_text.pdfminer.pdfminer_parse import PDFMinerParser
from server.services.pdf_to_text.pymupdf.pymupdf_parse import PymupdfParser
from server.services.pdf_to_text.abstract_pdf_to_text import PdfToTextParser

logger = structlog.get_logger()

__all__ = ["parse_pdf"]


def parse_pdf(file_path: str) -> str:
    """Attempts to parse PDF using PyMuPDF first, fallback to PDFMiner if needed."""

    parsers: list[PdfToTextParser] = [PymupdfParser(), PDFMinerParser()]

    logger.info(
        "starting PDF parsing",
        file=file_path,
        parsers=[p.__class__.__name__ for p in parsers],
    )

    for parser in parsers:
        try:
            logger.info("Trying parser", parser=parser.__class__.__name__)
            text = parser.parse(file_path)
            if text.strip():
                logger.info("Parser succeeded", parser=parser.__class__.__name__)
                return text
            logger.warning(
                "Parser returned empty text", parser=parser.__class__.__name__
            )
        except ValueError as e:
            logger.error(
                "Parser raised exception",
                parser=parser.__class__.__name__,
                error=str(e),
            )
            continue

    logger.error("All parsers failed", file=file_path)
    raise ValueError(
        f"Failed to extract text from PDF using available parsers: {file_path}"
    )
