"""This module merges data from two JSON files and groups it by page."""

import json
from rapidfuzz import fuzz


def merge_bboxes(bboxes):
    """Merges a list of bounding boxes into a single bounding box."""
    x0 = min(b[0] for b in bboxes)
    y0 = min(b[1] for b in bboxes)
    x1 = max(b[2] for b in bboxes)
    y1 = max(b[3] for b in bboxes)
    return [x0, y0, x1, y1]


# Load your files
with open(
    "/Users/raagarwal/Personal/resumate/server/test-poc/data.json",
    "r",
    encoding="utf-8",
) as f:
    semantic_data = json.load(f)  # This is a LIST

with open(
    "/Users/raagarwal/Personal/resumate/server/test-poc/data_extracted.json",
    "r",
    encoding="utf-8",
) as f:
    extracted_data = json.load(f)

semantic_items = []

# Flatten semantic JSON assuming it's a LIST of sections
for section in semantic_data:
    section_heading = section.get("heading", "")
    for subsection in section.get("subsections", []):
        sub_heading = subsection.get("heading", "")
        for idx, item in enumerate(subsection.get("content", {}).get("items", [])):
            # pylint: disable=invalid-name
            item_text = "".join(seg.get("text", "") for seg in item.get("segments", []))
            semantic_items.append(
                {
                    "section": section_heading,
                    "subsection": sub_heading,
                    "text": item_text.strip(),
                    "id": f"{section_heading}::{sub_heading}::{idx}",
                }
            )

# Also add paragraphs if present
for section in semantic_data:
    if section.get("content", {}).get("type") == "paragraph":
        semantic_items.append(
            {
                "section": section.get("heading", ""),
                "subsection": "",
                "text": section.get("content", {}).get("text", "").strip(),
                "id": f"{section.get('heading', '')}::paragraph",
            }
        )

# Build grouped output per page
output_pages = []

for page in extracted_data:
    page_number = page.get("page", 1)
    page_elements = []

    for sem_item in semantic_items:
        matched_lines = []
        for el in page.get("elements", []):
            if fuzz.partial_ratio(sem_item["text"], el["text"]) > 80:
                matched_lines.append(el)

        if matched_lines:
            merged_bbox = merge_bboxes([el["bbox"] for el in matched_lines])
            first_el = matched_lines[0]

            page_elements.append(
                {
                    "text": sem_item["text"],
                    "font": first_el.get("font", ""),
                    "size": first_el.get("size", 0),
                    "bbox": merged_bbox,
                    "color": first_el.get("color", 0),
                }
            )

    if page_elements:
        output_pages.append({"page": page_number, "elements": page_elements})

# Save final output
with open("final_grouped_output.json", "w", encoding="utf-8") as f:
    json.dump(output_pages, f, indent=2)

print("✅ Grouped JSON saved to final_grouped_output.json")
