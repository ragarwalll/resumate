"""This module extracts text and font information from a PDF file."""

import json
import fitz  # PyMuPDF


def extract_pdf_text_with_fonts(pdf_path, output_json="extracted_data.json"):
    """Extracts text and font information from a PDF file."""
    doc = fitz.open(pdf_path)
    extracted_data = []

    for page_num, page in enumerate(doc, start=1):
        page_data = {"page": page_num, "elements": []}
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    element = {
                        "text": span["text"],
                        "font": span["font"],
                        "size": span["size"],
                        "bbox": span["bbox"],  # (x0, y0, x1, y1)
                        "color": span["color"],
                    }
                    page_data["elements"].append(element)
        extracted_data.append(page_data)

    # Save extracted data to JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=2)

    print(f"Extraction complete! Data saved to {output_json}")


# Usage Example:
extract_pdf_text_with_fonts("assets/resume.pdf")
