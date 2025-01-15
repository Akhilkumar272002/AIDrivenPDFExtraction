# PDF Extractor with AI Model

---

## This is a PDF extractor with complex extracting with fine tuning processing of details

- The goal of this task is to extract borderless tables from PDF pages by combining PDF libraries with an LLM model to identify the patterns within these tables.

- Utilize the Pydantic AI framework.
Configure an LLM model that can effectively interpret PDF documents.

- Ensure the extraction accuracy of borderless tables is between 80-90%.

- `Example`: A PDF may contain text, tables, borderless tables, and images, making it challenging to identify borderless tables. The experimental solution involves recognizing patterns, such as word coordinates. The LLM model should understand these patterns and generate JSON data representing the borderless tables.