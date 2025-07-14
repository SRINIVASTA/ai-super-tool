import requests
import streamlit as st

# Load credentials from .streamlit/secrets.toml
GOOGLE_API_KEY = st.secrets["general"]["GOOGLE_API_KEY"]
GOOGLE_CSE_ID = st.secrets["general"]["GOOGLE_CSE_ID"]

def google_cse_search(query, num_results=3):
    """Performs a Google Custom Search and returns formatted results."""
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
