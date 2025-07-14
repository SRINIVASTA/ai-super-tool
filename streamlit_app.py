import streamlit as st
import os
from PIL import Image
import io
import google.generativeai as genai
from moviepy.editor import VideoFileClip
import pypdf
import docx
import pandas as pd

# ---------------------------
# Configure API keys & model
# ---------------------------

API_KEY = st.sidebar.text_input("Enter Google / Gemini API Key", type="password")
GOOGLE_CSE_ID = st.sidebar.text_input("Enter Google CSE ID", type="password")  # optional for search

if not API_KEY:
    st.warning("Please enter your API Key in the sidebar to proceed.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ---------------------------
# Helper Functions
# ---------------------------

def extract_content_from_file(file_path):
    content = ""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    try:
        if ext == '.pdf':
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                content += (page.extract_text() or "")
        elif ext == '.docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                content += para.text + "\n"
        elif ext == '.xlsx':
            xls = pd.ExcelFile(file_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                content += f"--- Sheet: {sheet_name} ---\n{df.to_string()}\n\n"
        elif ext in ['.csv', '.txt']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        else:
            return None, f"Unsupported file type: {ext}"
        if not content:
            return None, "No text could be extracted from the file."
        return content, None
    except Exception as e:
        return None, f"Error reading file: {e}"

def ask_a_question(query):
    prompt = f"Please provide a clear and well-explained answer to the following question: {query}"
    response = model.generate_content(prompt)
    return response.text

def generate_python_code(task_description):
    prompt = f"""Generate a complete, well-commented Python script for the following task. Do not include any explanations outside of the code comments. Task: {task_description}"""
    response = model.generate_content(prompt)
    return response.text.replace("```python", "").replace("```", "").strip()

def summarize_text(text):
    prompt = f"Please provide a short and simple summary of the following:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# ---------------------------------
# Streamlit UI
# ---------------------------------

st.title("🚀 AI Super Tool - Gemini + File Analysis + Image Gen")

tab = st.tabs(["AI Text Tools", "File Analysis", "Image Generation"])

# --- Tab 1: AI Text Tools ---
with tab[0]:
    st.header("Ask AI a Question")
    question = st.text_area("Enter your question here:")
    if st.button("Ask AI"):
        if question.strip():
            with st.spinner("Getting answer..."):
                answer = ask_a_question(question)
            st.success("Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

    st.markdown("---")
    st.header("Generate Python Code")
    task = st.text_area("Describe the Python coding task:")
    if st.button("Generate Code"):
        if task.strip():
            with st.spinner("Generating code..."):
                code = generate_python_code(task)
            st.success("Python code generated:")
            st.code(code, language='python')
        else:
            st.warning("Please describe a coding task.")

    st.markdown("---")
    st.header("Summarize Text")
    text_to_summarize = st.text_area("Enter text to summarize:")
    if st.button("Summarize"):
        if text_to_summarize.strip():
            with st.spinner("Summarizing..."):
                summary = summarize_text(text_to_summarize)
            st.success("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter some text.")

# --- Tab 2: File Analysis ---
with tab[1]:
    st.header("Upload a file for AI analysis")
    uploaded_file = st.file_uploader("Choose file", type=["pdf", "docx", "xlsx", "csv", "txt"])

    if uploaded_file:
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        content, error = extract_content_from_file(temp_file_path)

        if error:
            st.error(error)
        else:
            st.subheader("Extracted Content Preview:")
            st.text_area("File content", content, height=200)

            analysis_request = st.text_input("Analysis request", "Summarize this file. Describe its contents and key points.")

            if st.button("Analyze with AI"):
                with st.spinner("Analyzing file with AI..."):
                    response = model.generate_content([analysis_request, temp_file_path])
                st.subheader("AI Analysis Result:")
                st.write(response.text)

        # Clean up temp file
        os.remove(temp_file_path)

# --- Tab 3: Image Generation ---
with tab[2]:
    st.header("Generate an Image")

    prompt = st.text_input("Image prompt", "A majestic lion sitting on a throne, fantasy art")
    style = st.selectbox("Artistic Style", ["None", "Photorealistic", "Cartoon", "Oil Painting", "Watercolor", "Cyberpunk",
                                           "Steampunk", "Vintage", "Minimalist", "Fantasy", "Abstract", "Anime", "Impressionism"])
    aspect_ratio = st.selectbox("Aspect Ratio", ["Square (1:1)", "Landscape (16:9)", "Portrait (9:16)", "Standard (4:3)", "Widescreen (21:9)"])

    # Map aspect ratio to dimensions
    aspect_dims = {
        "Square (1:1)": (512, 512),
        "Landscape (16:9)": (768, 432),
        "Portrait (9:16)": (432, 768),
        "Standard (4:3)": (680, 512),
        "Widescreen (21:9)": (896, 384)
    }

    output_format = st.selectbox("Output Format", ["PNG", "JPEG", "PDF", "BMP", "TIFF"])
    filename = st.text_input("Save filename (without extension)", "generated_image")

    if st.button("Generate Image"):
        if not prompt.strip():
            st.warning("Please enter an image prompt.")
        else:
            try:
                from diffusers import StableDiffusionPipeline
                import torch

                device = "cuda" if torch.cuda.is_available() else "cpu"
                pipe = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                )
                pipe = pipe.to(device)

                full_prompt = prompt
                if style != "None":
                    full_prompt += f", {style} style"

                width, height = aspect_dims[aspect_ratio]

                with st.spinner("Generating image..."):
                    image = pipe(full_prompt, width=width, height=height).images[0]

                ext = output_format.lower()
                save_path = f"{filename}.{ext}"

                if output_format == "PDF":
                    image.convert("RGB").save(save_path)
                else:
                    image.save(save_path)

                st.success(f"Image saved as {save_path}")
                st.image(image)

            except Exception as e:
                st.error(f"Image generation error: {e}")
