import streamlit as st
import requests
import google.generativeai as genai

# Sidebar: Enter only one API key
st.sidebar.title("Enter Your API Key")
API_KEY = st.sidebar.text_input("Google / Gemini API Key", type="password")

# Also need Google CSE ID for search (separate)
GOOGLE_CSE_ID = st.sidebar.text_input("Google CSE ID")

if not API_KEY or not GOOGLE_CSE_ID:
    st.warning("Please enter both the API key and the Google CSE ID in the sidebar.")
    st.stop()

# Configure Gemini AI with the single API key
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error configuring Gemini AI: {e}")
    st.stop()

# Define Gemini AI functions (same as before)

def ask_a_question(query):
    prompt = f"Please provide a clear and well-explained answer to the following question: {query}"
    response = model.generate_content(prompt)
    return response.text

def translate_text(text, target_language):
    prompt = f"Translate the following text to {target_language}. Only provide the translated text: '{text}'"
    response = model.generate_content(prompt)
    return response.text

def generate_python_code(task_description):
    prompt = f"""Generate a complete, well-commented Python script for the following task. Do not include any explanations outside of the code comments. Task: {task_description}"""
    response = model.generate_content(prompt)
    code_block = response.text.replace("```python", "").replace("```", "").strip()
    return code_block

def summarize_text(text):
    prompt = f"Please provide a short and simple summary of the following:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# Google Custom Search using same API_KEY + CSE ID
def google_cse_search(query, num_results=3):
    params = {
        "key": API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": num_results
    }
    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
    data = response.json()

    if "items" not in data:
        return f"❌ Error: {data.get('error', {}).get('message', 'No results')}"

    results = []
    for item in data["items"]:
        title = item.get("title")
        snippet = item.get("snippet")
        link = item.get("link")
        results.append(f"🔹 **{title}**\n{snippet}\n🔗 {link}\n")

    return "\n".join(results)

# UI
tool = st.sidebar.selectbox("Select AI Tool", [
    "Ask a Question",
    "Translate Text",
    "Generate Python Code",
    "Summarize Text",
    "Google Search"
])

if tool == "Ask a Question":
    question = st.text_area("Enter your question:")
    if st.button("Get Answer"):
        if question.strip():
            answer = ask_a_question(question)
            st.markdown("### AI Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

elif tool == "Translate Text":
    text_to_translate = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Target Language", ["Spanish", "French", "German", "Japanese", "Italian"])
    if st.button("Translate"):
        if text_to_translate.strip():
            translation = translate_text(text_to_translate, target_language)
            st.markdown(f"### Translation to {target_language}:")
            st.write(translation)
        else:
            st.warning("Please enter text to translate.")

elif tool == "Generate Python Code":
    task_description = st.text_area("Describe the Python coding task:")
    if st.button("Generate Code"):
        if task_description.strip():
            code = generate_python_code(task_description)
            st.markdown("### Generated Python Code:")
            st.code(code, language='python')
        else:
            st.warning("Please describe the coding task.")

elif tool == "Summarize Text":
    text_to_summarize = st.text_area("Enter text to summarize:")
    if st.button("Summarize"):
        if text_to_summarize.strip():
            summary = summarize_text(text_to_summarize)
            st.markdown("### Summary:")
            st.write(summary)
        else:
            st.warning("Please enter text to summarize.")

elif tool == "Google Search":
    query = st.text_input("Enter Google search query:")
    if st.button("Search"):
        if query.strip():
            results = google_cse_search(query)
            st.markdown("### Search Results:")
            st.markdown(results)
        else:
            st.warning("Please enter a search query.")
