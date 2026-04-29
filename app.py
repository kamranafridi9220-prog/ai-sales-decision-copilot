import os
import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI Sales Decision Copilot", layout="wide")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🚀 AI Sales Decision Copilot")
st.write("Upload your dataset, ask a business question, and get AI-powered decision insights.")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

def ask_ai(question, data_preview):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a business decision analyst. Provide structured insights from data."},
            {"role": "user", "content": f"""
Dataset preview:
{data_preview}

Question:
{question}

Provide:
- Key insight
- Business implication
- Recommendation
- Confidence level (Low/Medium/High)
- Next best action
"""}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Ask a Business Question")
    user_question = st.text_input("Example: Which segment should we focus on for growth?")

    if st.button("Generate Decision Insight"):
        if user_question:
            with st.spinner("Analyzing data..."):
                preview_text = df.head(20).to_string()
                result = ask_ai(user_question, preview_text)

            st.subheader("AI Decision Insight")
            st.write(result)

        else:
            st.warning("Please enter a question.")
else:
    st.info("Upload a dataset to begin.")
