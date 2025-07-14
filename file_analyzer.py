import os
import pypdf
import docx
import pandas as pd

def extract_content_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    content = ""
    try:
        if file_extension.lower() == '.pdf':
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                content += page.extract_text() or ""
        elif file_extension.lower() == '.docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                content += para.text + "\n"
        elif file_extension.lower() == '.xlsx':
            xls = pd.ExcelFile(file_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                content += f"--- Sheet: {sheet_name} ---\n{df.to_string()}\n\n"
        elif file_extension.lower() in ['.csv', '.txt']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        else:
            return None, f"Unsupported file type: {file_extension}"
        if not content:
            return None, "No text could be extracted from the file."
        return content, None
    except Exception as e:
        return None, f"An error occurred while reading the file: {e}"
