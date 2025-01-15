# image extractor using PyMuPDF(fitz)

import fitz  # PyMuPDF
import os

def extract_images(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    image_data = {}
    image_count = 1
    doc = fitz.open(pdf_path)
    for page in doc:
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
    return image_data