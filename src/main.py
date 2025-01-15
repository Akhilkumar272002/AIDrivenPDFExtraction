# main file

import os
import json
from config import OUTPUT_DIR, OUTPUT_JSON
from extractors.text_extractor import extract_text
from extractors.table_extractor import extract_tables
from extractors.image_extractor import extract_images

def main(pdf_path):
    # Ensure output directories exist
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    # Extract data
    text_data = extract_text(pdf_path)
    table_data = extract_tables(pdf_path)
    image_data = extract_images(pdf_path, OUTPUT_DIR)

    # Combine into JSON
    combined_data = {**text_data, **table_data, **image_data}

    # Save JSON output
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4)

    print(f"Extraction complete. JSON saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    pdf_path = "input_pdfs/PDFtest.pdf"  # Replace with your PDF path
    main(pdf_path)