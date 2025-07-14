import streamlit as st
from ai_tools import ask_a_question, translate_text, generate_python_code, summarize_text
from file_analyzer import extract_content_from_file
from google_search import google_cse_search
from image_generator import generate_image_from_prompt

st.title("AI Super Tool")

tool = st.sidebar.selectbox("Choose an AI Tool", [
    "Ask a Question",
    "Translate Text",
    "Generate Python Code",
    "Summarize Text",
    "Analyze Uploaded File",
    "Google Search",
    "Generate AI Image"
])

if tool == "Ask a Question":
    query = st.text_input("Enter your question:")
    if st.button("Ask"):
        answer = ask_a_question(query)
        st.write(answer)

elif tool == "Translate Text":
    text = st.text_area("Text to translate:")
    lang = st.selectbox("Target language:", ["Spanish", "French", "German", "Japanese", "Italian"])
    if st.button("Translate"):
        translation = translate_text(text, lang)
        st.write(translation)

elif tool == "Generate Python Code":
    task = st.text_area("Describe the task for Python code:")
    if st.button("Generate Code"):
        code = generate_python_code(task)
        st.code(code, language='python')

elif tool == "Summarize Text":
    text = st.text_area("Text to summarize:")
    if st.button("Summarize"):
        summary = summarize_text(text)
        st.write(summary)

elif tool == "Analyze Uploaded File":
    uploaded_file = st.file_uploader("Upload a file")
    analysis_request = st.text_area("What analysis do you want on the file?")
    if uploaded_file and st.button("Analyze"):
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        content, error = extract_content_from_file(uploaded_file.name)
        if error:
            st.error(error)
        else:
            st.text_area("Extracted content preview:", content[:1000])
            st.success("File content extracted successfully.")

elif tool == "Google Search":
    query = st.text_input("Search query:")
    if st.button("Search"):
        results = google_cse_search(query)
        st.markdown(results)

elif tool == "Generate AI Image":
    prompt = st.text_input("Image prompt:")
    style = st.selectbox("Style", ["None", "Photorealistic", "Cartoon", "Oil Painting", "Fantasy"])
    aspect_ratio = st.selectbox("Aspect Ratio", [
        "Square (1:1)", "Landscape (16:9)", "Portrait (9:16)", "Standard (4:3)", "Widescreen (21:9)"
    ])
    if st.button("Generate Image"):
        image = generate_image_from_prompt(prompt, style, aspect_ratio)
        st.image(image)
