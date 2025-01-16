import os
import json
import fitz  # PyMuPDF
from config import OUTPUT_DIR, OUTPUT_JSON

def extract_bordered_tables_from_page(page, table_count):
    table_data = {}
    excluded_bboxes = []

    # Extract the text and layout information using the 'dict' method
    page_dict = page.get_text("dict")
    lines = page_dict.get("lines", [])  # Extract lines from the page

    if lines:
        # Sort lines based on their Y-coordinate to group horizontal and vertical lines
        horizontal_lines = [line for line in lines if abs(line[1] - line[3]) < 1]  # Lines where y1 == y2 (horizontal)
        vertical_lines = [line for line in lines if abs(line[0] - line[2]) < 1]    # Lines where x1 == x2 (vertical)

        # We can group these lines into table rows and columns based on their proximity
        row_lines = sorted(horizontal_lines, key=lambda x: x[1])  # Sort by Y-coordinate (horizontal lines)
        col_lines = sorted(vertical_lines, key=lambda x: x[0])   # Sort by X-coordinate (vertical lines)

        # Now we have row_lines and col_lines; group the words based on these rows and columns
        table_cells = []
        for y1, y2 in zip(row_lines[:-1], row_lines[1:]):  # Iterate through pairs of horizontal lines
            for x1, x2 in zip(col_lines[:-1], col_lines[1:]):  # Iterate through pairs of vertical lines
                # Map words to the table grid
                cell_words = []
                for word in page.get_text("words"):
                    if x1 <= word[0] <= x2 and y1 <= word[1] <= y2:
                        cell_words.append(word[4])  # word[4] is the text part of the tuple
                table_cells.append(cell_words)

        # Format the table data for output
        formatted_table = {f"row{row_index}": cell for row_index, cell in enumerate(table_cells)}
        table_data[f"table{table_count}"] = formatted_table
        table_count += 1

    return table_data, excluded_bboxes, table_count

def extract_borderless_tables_from_page(page, table_count):
    table_data = {}
    excluded_bboxes = []
    
    # Extract text from the page to detect borderless tables
    words = page.get_text("words")  # Corrected method
    if words:
        current_table = []
        row = []
        previous_y = None

        for word in words:
            y = word[1]  # word[1] is the 'top' coordinate
            if previous_y and abs(y - previous_y) > 5:  # New row detected if there's a big gap
                if row:
                    current_table.append(row)
                    row = []
            row.append(word[4])  # word[4] is the text part of the tuple
            previous_y = y
        
        if row:  # Add the last row
            current_table.append(row)
        
        table_data[f"table{table_count}"] = current_table
        table_count += 1

    return table_data, excluded_bboxes, table_count

def extract_images_from_page(page, doc, image_count, output_dir):
    image_data = {}
    for img_index, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        image_filename = f"image{image_count}.{image_ext}"
        image_path = os.path.join(output_dir, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)

        image_data[f"image{image_count}"] = image_filename
        image_count += 1
    return image_data, image_count

def extract_text_from_page(page, excluded_bboxes, text_count):
    text_data = {}
    for word in page.get_text("words"):
        word_bbox = (word[0], word[1], word[2], word[3])
        # Exclude text overlapping with any table bounding box
        if not any(
            word_bbox[0] < bbox[2] and word_bbox[2] > bbox[0] and
            word_bbox[1] < bbox[3] and word_bbox[3] > bbox[1]
            for bbox in excluded_bboxes
        ):
            text_data[f"text{text_count}"] = word[4]  # word[4] is the text part of the tuple
            text_count += 1
    return text_data, text_count

def main(pdf_path):
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    combined_data = {}
    image_count = 1
    text_count = 1
    table_count = 1

    with fitz.open(pdf_path) as doc:
        for page_number, page in enumerate(doc, start=1):
            page_elements = {}

            # Extract bordered tables
            bordered_tables, excluded_bboxes, table_count = extract_bordered_tables_from_page(page, table_count)
            page_elements.update(bordered_tables)

            # Extract borderless tables
            borderless_tables, excluded_bboxes, table_count = extract_borderless_tables_from_page(page, table_count)
            page_elements.update(borderless_tables)

            # Extract text
            text, text_count = extract_text_from_page(page, excluded_bboxes, text_count)
            page_elements.update(text)

            # Extract images
            images, image_count = extract_images_from_page(page, doc, image_count, OUTPUT_DIR)
            page_elements.update(images)

            combined_data[f"page_{page_number}"] = page_elements

    # Save JSON output
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4)

    print(f"Extraction complete. JSON saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    pdf_path = "input_pdfs/PDFtest.pdf"  # Replace with your PDF path
    main(pdf_path)
