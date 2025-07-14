import streamlit as st
import requests
import google.generativeai as genai

# Sidebar for API key inputs
st.sidebar.title("Enter Your API Keys")

GOOGLE_API_KEY = st.sidebar.text_input("Google API Key", type="password")
GOOGLE_CSE_ID = st.sidebar.text_input("Google CSE ID", type="password")
GEMINI_API_KEY = st.sidebar.text_input("Gemini API Key", type="password")

# Stop if any keys are missing
if not (GOOGLE_API_KEY and GOOGLE_CSE_ID and GEMINI_API_KEY):
    st.warning("Please enter all API keys in the sidebar to continue.")
    st.stop()

# Configure Gemini AI with entered API key
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error configuring Gemini AI: {e}")
    st.stop()

# Function for Google Custom Search
def google_cse_search(query, num_results=3):
    params = {
        "key": GOOGLE_API_KEY,
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

# --- UI Tabs for different tools ---

tab = st.sidebar.radio("Select Tool", ["Ask AI", "Google Search"])

if tab == "Ask AI":
    question = st.text_area("Ask a question to Gemini AI:")
    if st.button("Get Answer"):
        if question.strip():
            prompt = f"Please provide a clear and well-explained answer to the following question: {question}"
            response = model.generate_content(prompt)
            st.markdown("### AI Answer:")
            st.write(response.text)
        else:
            st.warning("Please enter a question.")

elif tab == "Google Search":
    query = st.text_input("Enter your Google search query:")
    if st.button("Search"):
        if query.strip():
            results = google_cse_search(query)
            st.markdown("### Search Results:")
            st.markdown(results)
        else:
            st.warning("Please enter a search query.")
