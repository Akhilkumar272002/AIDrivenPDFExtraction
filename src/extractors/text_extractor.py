# text extractor using pdfplumber

import pdfplumber

def extract_text(pdf_path):
    text_data = {}
    text_count = 1
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_data[f"text{text_count}"] = text.strip()
                text_count += 1
    return text_data
