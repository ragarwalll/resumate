"""Tests for the PDF parser classes."""

import os
import pytest
from server.services.pdf_to_text.pdfminer.pdfminer_parse import PDFMinerParser
from server.services.pdf_to_text.pymupdf.pymupdf_parse import PymupdfParser
from server.__tests__.constants import TEST_PDF


@pytest.mark.parametrize("parser_class", [PDFMinerParser, PymupdfParser])
def test_pdf_parser_extracts_text(parser_class):
    """Tests that the PDF parser extracts text from a PDF file."""
    parser = parser_class()
    assert os.path.exists(TEST_PDF), f"Test file not found: {TEST_PDF}"

    text = parser.parse(TEST_PDF)

    assert isinstance(text, str), "Parsed text should be a string"
    assert len(text.strip()) > 0, "Parsed text should not be empty"
    assert (
        "Resume generated using Vitagen" in text
    ), "Expected text not found in parsed content"
