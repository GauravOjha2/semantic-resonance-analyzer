import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# --- 1. SETUP & SECURE API KEY LOADING ---
# This part is working perfectly. No changes needed.
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash-lite') 
except Exception as e:
    st.error("🔴 Error: Your Google API Key is not set correctly in the Streamlit Secrets. Please add it.")
    st.stop()


# --- 2. THE MASTER SYNTHESIS FUNCTION ---
def get_final_report(top_pairs_df):
    raw_analysis_text = ""
    for index, row in top_pairs_df.iterrows():
        raw_analysis_text += f"Similarity Score: {row['CrossEncoderScore']:.4f}\n"
        raw_analysis_text += f"Adam's Post: {row['PostA']}\n"
        raw_analysis_text += f"Kenji's Post: {row['PostB']}\n---\n"

    # --- ⭐️ THIS IS THE CORRECTED PROMPT ⭐️ ---
    # We have removed the conversational parts and made it a direct command.
    master_prompt = f"""
You are a world-class relationship psychologist. Your task is to synthesize the provided raw analysis data into a holistic compatibility report.

**RAW ANALYSIS DATA:**
---
{raw_analysis_text}
---

**YOUR COMMAND:**
Based ONLY on the raw data provided, generate the final compatibility report. You must use the following exact format and Markdown. Do not add any introductory text or conversational replies.

### Overall Compatibility Score:
[Provide a qualitative score like "High," "Moderate," or "Surprisingly High Potential"]

### The Foundation: Shared Passions
[Write a paragraph describing their shared interests based on the data.]

### The Spark: Exploring Differences
[Write a paragraph about their unique interests based on the data.]

### Communication Dynamics: How They Might Interact
[Write a paragraph analyzing their communication styles based on the data.]

### Final Verdict & Conversation Starters
[Write a concluding paragraph summarizing their potential connection and provide 3-5 concrete conversation starters based on the data.]
"""
    # --- END OF PROMPT CORRECTION ---
    
    try:
        response = model.generate_content(master_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error during API call: {e}"

# --- 3. STREAMLIT USER INTERFACE (No changes needed) ---
st.set_page_config(layout="wide")
st.title("Semantic Resonance Analyzer 🔮")
st.write("Discover the hidden connections between Adam Savage and Kenji López-Alt.")

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
        top_pairs = df_sorted.head(30)
        final_report = get_final_report(top_pairs)
        
        st.markdown("---")
        st.markdown(final_report)

st.sidebar.info("This app analyzes the pre-computed semantic similarity scores of ~17,400 post pairs to generate a holistic compatibility report.")
st.sidebar.dataframe(df_results.head())

