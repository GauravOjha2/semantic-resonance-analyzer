import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# --- 1. SETUP & SECURE API KEY LOADING ---
# We will load the API key from Streamlit's "Secrets" management.
# This is the professional and secure way to handle keys.
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # This is the model name you discovered that works!
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    # This will show a nice error message if the secret is not set.
    st.error("🔴 Error: Your Google API Key is not set correctly in the Streamlit Secrets. Please add it.")
    st.stop()


# --- 2. THE MASTER SYNTHESIS FUNCTION ---
# This function takes the top pairs and generates the final report with one API call.
def get_final_report(top_pairs_df):
    raw_analysis_text = ""
    for index, row in top_pairs_df.iterrows():
        raw_analysis_text += f"Similarity Score: {row['CrossEncoderScore']:.4f}\n"
        raw_analysis_text += f"Adam's Post: {row['PostA']}\n"
        raw_analysis_text += f"Kenji's Post: {row['PostB']}\n---\n"

    master_prompt = f"""
    You are a world-class relationship psychologist... (Your full Master Prompt here)
    ... (rest of your Master Prompt)
    """
    
    try:
        response = model.generate_content(master_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error during API call: {e}"

# --- 3. STREAMLIT USER INTERFACE ---
st.set_page_config(layout="wide")
st.title("Semantic Resonance Analyzer 🔮")
st.write("Discover the hidden connections between Adam Savage and Kenji López-Alt.")

# Load the pre-computed cross-encoder results
# This function caches the data so it only loads once.
@st.cache_data
def load_data():
    try:
        return pd.read_csv("cross_encoder_results.csv")
    except FileNotFoundError:
        return None

df_results = load_data()

if df_results is None:
    st.error("🔴 Error: `cross_encoder_results.csv` not found. Please make sure it's in your GitHub repository.")
    st.stop()

if st.button("Analyze Their Connection", type="primary"):
    with st.spinner("Finding the most resonant interactions and synthesizing the final report..."):
        df_sorted = df_results.sort_values(by="CrossEncoderScore", ascending=False)
        top_pairs = df_sorted.head(30) # Select the top 30 most similar pairs
        final_report = get_final_report(top_pairs)
        
        st.markdown("---")
        st.markdown(final_report)

st.sidebar.info("This app analyzes the pre-computed semantic similarity scores of ~17,400 post pairs to generate a holistic compatibility report.")
st.sidebar.dataframe(df_results.head())