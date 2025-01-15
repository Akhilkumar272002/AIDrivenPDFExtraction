# table extractor using camelot

import camelot

def extract_tables(pdf_path):
    table_data = {}
    table_count = 1
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", strip_text='')
        for table in tables:
            formatted_table = table.df.to_dict(orient="index")
            table_data[f"table{table_count}"] = formatted_table
            table_count += 1
    except Exception as e:
        print(f"Error extracting tables: {e}")
    return table_data