import google.generativeai as genai
from google.colab import userdata

try:
    API_KEY = userdata.get('GOOGLE_API_KEY')
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    # fallback or raise error
    pass

def ask_a_question(query):
    prompt = f"Please provide a clear and well-explained answer to the following question: {query}"
    response = model.generate_content(prompt)
    return response.text

def translate_text(text, target_language):
    prompt = f"Translate the following text to {target_language}. Only provide the translated text: '{text}'"
    response = model.generate_content(prompt)
    return response.text

def generate_python_code(task_description):
    prompt = f"Generate a complete, well-commented Python script for the following task. Do not include any explanations outside of the code comments. Task: {task_description}"
    response = model.generate_content(prompt)
    code_block = response.text.replace("```python", "").replace("```", "").strip()
    return code_block

def summarize_text(text):
    prompt = f"Please provide a short and simple summary of the following:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text
