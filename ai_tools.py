import streamlit as st
import google.generativeai as genai
import pandas as pd
import pypdf
import docx
import os

# --- Configuration: Load API key from secrets ---
try:
    API_KEY = st.secrets["general"]["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ Error configuring Gemini: {e}")
    model = None

# --- General AI Tools ---

def ask_a_question(query):
    """Ask Gemini a general question."""
    prompt = f"Please provide a clear and well-explained answer to the following question: {query}"
    response = model.generate_content(prompt)
    return response.text

def translate_text(text, target_language):
    """Translate text using Gemini."""
    prompt = f"Translate the following text to {target_language}. Only provide the translated text: '{text}'"
    response = model.generate_content(prompt)
    return response.text

def generate_python_code(task_description):
    """Generate Python code for a given task."""
    prompt = (
        f"Generate a complete, well-commented Python script for the following task. "
        f"Do not include any explanations outside of the code comments. Task: {task_description}"
    )
    response = model.generate_content(prompt)
    return response.text.replace("```python", "").replace("```", "").strip()

def summarize_text(text):
    """Summarize input text."""
    prompt = f"Please provide a short and simple summary of the following:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# --- File Analyzer ---

def extract_content_from_file(file_path):
    """Extract text content from PDF, DOCX, XLSX, CSV, or TXT."""
    _, file_extension = os.path.splitext(file_path)
    content = ""
    try:
        if file_extension.lower() == '.pdf':
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                content += (page.extract_text() or "")
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
        return None, f"Error reading file: {e}"
