# Semantic Resonance Analyzer 🔮

**Author:** [Gaurav Ojha](https://www.linkedin.com/in/gauravojha1/)  
**Live Application:** [**semantic-resonance-analyzer.streamlit.app**](https://semantic-resonance-analyzer-q3s5m3neestnazca6cqzoc.streamlit.app/)  
**GitHub:** [**GauravOjha2/semantic-resonance-analyzer**](https://github.com/GauravOjha2/semantic-resonance-analyzer)

---

## The Vision: Can AI Understand Human Connection?

This project was born from a single, ambitious question: What if we could use AI to understand the deep, hidden connections between two people, far beyond simple keyword matching?

The **Semantic Resonance Analyzer** is a multi-stage AI pipeline that ingests the public text feeds of two individuals and generates a holistic, psychological report on their potential compatibility. It doesn't just look at *what* they talk about, but *how* they think, reason, and communicate.

To prove this concept, I chose two of my favorite creators: **Adam Savage** (`u/mistersavage`) and **J. Kenji López-Alt** (`u/J_Kenji_Lopez-Alt`). One is a master of the workshop, the other a master of the kitchen. This project's goal was to find the "semantic resonance" in their shared, underlying passion for craftsmanship, scientific methodology, and meticulous experimentation.

<img width="1738" height="917" alt="{1B92C229-4BEC-43B3-BF14-CEA5ED29A8BD}" src="https://github.com/user-attachments/assets/189505f8-ed88-4e46-8b0a-0147e370333b" />

---

## The Engineering Journey: From Brute Force to a Resilient Pipeline

Building this project was a real-world lesson in engineering resilience. The initial vision of a fully dynamic app quickly met the hard realities of compute limits, API instability, and complex development environments.

*   **The Compute Barrier:** The initial analysis required scoring over **17,400 unique pairs** of comments. Running this on-demand for a live web app was computationally impossible. This led to the core architectural decision: a two-phase "offline analysis, live synthesis" pipeline.

*   **The API Labyrinth:** The journey to a stable generative model was fraught with challenges.
    *   **Google Cloud's Free Trial** system proved to be an opaque and frustrating maze of project permissions, regional model unavailability, and confusing billing setups.
    *   The free-tier **Google AI Studio API** was unstable, with model names working one day and returning `404 Not Found` errors the next, proving it was not suitable for a reliable application.

*   **The Local Model Wall:** As an alternative, I explored running a powerful, open-source LLM locally. This led to its own set of challenges, including `llama-cpp-python` build failures in the Colab environment due to deep-seated dependency issues.

This journey forced a series of professional engineering pivots, resulting in a final architecture that is robust, efficient, and tells a compelling story of its own.

---

## 🧠 Final Project Architecture

The final application is a testament to this journey, combining a powerful offline analysis pipeline with a lightweight, interactive web application.

### Phase 1: Offline Data Pipeline

1.  **Data Scraping (`scrape_reddit_data.py`):** The pipeline begins by using Python and the **PRAW** library to scrape the ~200 most recent comments and posts from the two target users. This data is cleaned and saved to CSV files. The script is designed for security, loading Reddit API credentials from a `.env` file (which is ignored by Git).

2.  **Deep Semantic Analysis (`run_cross_encoder_analysis.py`):** This is the core of the analysis. Instead of a faster but less accurate Bi-Encoder, I chose a **Cross-Encoder** (`cross-encoder/ms-marco-MiniLM-L-6-v2`). This model processes both posts in a pair *simultaneously*, yielding a highly accurate and context-aware similarity score between -12 and +12. This script processes all **17,400+ pairs**, a computationally intensive task that justifies the offline approach. The results are saved to `cross_encoder_results.csv`.

### Phase 2: Live Synthesis (The Deployed App)

1.  **Load Pre-computed Data:** The live Streamlit app (`app.py`) instantly loads the `cross_encoder_results.csv` file, which serves as its knowledge base.

2.  **Find the Resonance:** When the user clicks "Analyze," the app sorts the data and selects the **Top 30 pairs** with the highest similarity scores. These pairs represent the strongest points of connection and serve as the "evidence" for the final report.

3.  **The Master Prompt & Synthesis:** The evidence is formatted into a sophisticated **"Master Prompt"** which instructs a powerful LLM to act as a relationship psychologist. A single, efficient API call is made to the stable **Google Gemini API** (`gemini-1.5-flash`), which synthesizes the evidence into the final, holistic report.

---

## 🛠️ Tech Stack

*   **Data Scraping & Processing:** Python, PRAW, Pandas, NumPy
*   **Machine Learning / AI:**
    *   **Semantic Analysis:** `sentence-transformers` (Cross-Encoder)
    *   **Generative Synthesis:** Google Gemini API (`gemini-1.5-flash`)
    *   **Local Alternative:** Mistral-7B (GGUF Quantized) with `llama-cpp-python`
*   **Frontend & Deployment:** Streamlit, Streamlit Community Cloud
*   **Development:** VS Code, Google Colab, Git & GitHub

---

## 🚀 How to Run

### Live App

The easiest way to see the project is to visit the live application:
➡️ [**semantic-resonance-analyzer.streamlit.app**](https://semantic-resonance-analyzer-q3s5m3neestnazca6cqzoc.streamlit.app/)

### Replicating the Pipeline Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/GauravOjha2/semantic-resonance-analyzer.git
    cd semantic-resonance-analyzer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Offline Analysis (Optional):**
    *   To re-generate the data from scratch, you will first need to run the scraping script (`scrape_reddit_data.py`) and then the cross-encoder analysis (`run_cross_encoder_analysis.py`). *Note: The cross-encoder script is computationally intensive and will be much faster with a CUDA-enabled GPU.*

4.  **Run the Streamlit app:**
    *   To run the live app (which uses the pre-computed data), first set up your API key. Create a file named `.env` and add your Google AI Studio key: `GOOGLE_API_KEY="YOUR_KEY_HERE"`
    *   Then, run the app:
    ```bash
    streamlit run app.py
    ```

## 🔬 The "Director's Cut": 100% Free, Local Model Version

I believe in open-source and demonstrating solutions that work without financial barriers. I have created a **Google Colab notebook** that contains the entire synthesis pipeline, running **100% locally and for free** using a quantized version of the powerful Mistral-7B model.

This notebook is a runnable tutorial that tells the project's story and serves as a powerful proof-of-concept for a fully open-source version of this analyzer.

➡️ **[https://colab.research.google.com/drive/1Xag3NDKdTNhl4pDnN194pww023Fv_5V9#]** 
## 🤝 Connect with Me

This project was a challenging and incredibly rewarding journey into the heart of modern AI engineering. If you have any questions or would like to connect, please feel free to reach out.

*   **LinkedIn:** [**linkedin.com/in/gauravojha1/**](https://www.linkedin.com/in/gauravojha1/)
