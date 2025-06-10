#code without API
import fitz  
from docx import Document
from PIL import Image
import pytesseract
import pandas as pd
import re
import difflib
import pdfplumber

from model_interface import query_llm

def extract_text(file_path):
    ext = file_path.split('.')[-1].lower()
    
    if ext == 'pdf':
        doc = fitz.open(file_path)
        return "\n".join([page.get_text() for page in doc])
    
    elif ext == 'docx':
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    elif ext in ['jpg', 'jpeg', 'png']:
        return pytesseract.image_to_string(Image.open(file_path))
    
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    else:
        return "Unsupported file type"

def structure_data(text):
    # Try to extract key-value pairs (multi-line values)
    pattern = re.compile(r'([^\n:]+):\s*([^\n]+(?:\n(?![^\n:]+:).+)*)')
    matches = pattern.findall(text)
    if matches:
        # Clean up values (remove extra newlines)
        data = [{"Field": k.strip(), "Value": v.replace('\n', ' ').strip()} for k, v in matches]
        return pd.DataFrame(data)
    else:
        # No structured data found, return raw text
        return pd.DataFrame([{"Field": "Raw Text", "Value": text}])

def query_data(text, query):
    prompt = f"""
You are a data analysis tool. Use the following information:

{text}

Now answer the question: {query}
"""
    return query_llm(prompt)

def query_structured_data(structured_df, query):
    if not query:
        return None
    # Lowercase all fields for comparison
    fields = [str(f).lower() for f in structured_df['Field']]
    # Try to find the best match for the query in the fields
    best_matches = difflib.get_close_matches(query.lower(), fields, n=1, cutoff=0.5)
    if best_matches:
        match = best_matches[0]
        value = structured_df[structured_df['Field'].str.lower() == match]['Value'].values[0]
        return f"{match.title()}: {value}"
    else:
        return "Requested information not found in structured data."

def extract_tables_from_pdf(file_path):
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables_on_page = page.extract_tables()
            for table in tables_on_page:
                tables.append(table)  # Each table is a list of lists (rows)
    return tables  # This is a list of DataFrames

def analyze_document(file_path, query):
    raw_text = extract_text(file_path)
    structured = structure_data(raw_text)
    # If structured is a DataFrame, use local query
    if isinstance(structured, pd.DataFrame):
        response = query_structured_data(structured, query)
    else:
        response = "Structured data is not in DataFrame format."
    tables = []
    # Optionally: extract tables if PDF
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        tables = extract_tables_from_pdf(file_path)
    return structured, response, tables

