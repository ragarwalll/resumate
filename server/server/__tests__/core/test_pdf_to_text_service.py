"""Tests for the PDF parsing service."""

from unittest.mock import patch, MagicMock
import pytest
from server.core import parse_pdf
from server.__tests__.constants import TEST_PDF


def test_parse_pdf_success_with_first_parser():
    """Should return text when first parser succeeds"""
    mock_first = MagicMock()
    mock_first.parse.return_value = "Parsed text from first parser"

    mock_second = MagicMock()

    with (
        patch("server.core.pdf_parser.PymupdfParser", return_value=mock_first),
        patch("server.core.pdf_parser.PDFMinerParser", return_value=mock_second),
    ):
        result = parse_pdf(TEST_PDF)
        assert result == "Parsed text from first parser"
        mock_first.parse.assert_called_once()
        mock_second.parse.assert_not_called()


def test_parse_pdf_success_with_second_parser():
    """Should return text when first parser fails but second succeeds"""
    mock_first = MagicMock()
    mock_first.parse.side_effect = Exception("First parser failed")

    mock_second = MagicMock()
    mock_second.parse.return_value = "Parsed text from second parser"

    with (
        patch("server.core.pdf_parser.PymupdfParser", return_value=mock_first),
        patch("server.core.pdf_parser.PDFMinerParser", return_value=mock_second),
    ):
        result = parse_pdf(TEST_PDF)
        assert result == "Parsed text from second parser"
        mock_first.parse.assert_called_once()
        mock_second.parse.assert_called_once()


def test_parse_pdf_raises_error_when_all_fail():
    """Should raise ValueError when all parsers fail"""
    mock_first = MagicMock()
    mock_first.parse.side_effect = Exception("First parser failed")

    mock_second = MagicMock()
    mock_second.parse.side_effect = Exception("Second parser failed")

    with (
        patch("server.core.pdf_parser.PymupdfParser", return_value=mock_first),
        patch("server.core.pdf_parser.PDFMinerParser", return_value=mock_second),
    ):
        with pytest.raises(ValueError, match="Failed to extract text from PDF"):
            parse_pdf(TEST_PDF)
        mock_first.parse.assert_called_once()
        mock_second.parse.assert_called_once()
