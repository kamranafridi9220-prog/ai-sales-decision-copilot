import os
import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(
    page_title="AI Sales Decision Copilot",
    page_icon="🚀",
    layout="wide"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🚀 AI Sales Decision Copilot")
st.write("Upload your dataset, ask a business question, and get AI-powered decision insights.")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])


def ask_ai(question, data_preview):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a business decision analyst. Always respond in clearly separated sections."
            },
            {
                "role": "user",
                "content": f"""
Dataset preview:
{data_preview}

Question:
{question}

Respond in this EXACT format:

Key Insight:
...

Business Implication:
...

Recommendation:
...

Confidence Level:
...

Next Best Action:
...
"""
            }
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def parse_response(text):
    sections = {
        "Key Insight": "",
        "Business Implication": "",
        "Recommendation": "",
        "Confidence Level": "",
        "Next Best Action": ""
    }

    current_section = None

    for line in text.split("\n"):
        line = line.strip()

        if line.startswith("Key Insight"):
            current_section = "Key Insight"
        elif line.startswith("Business Implication"):
            current_section = "Business Implication"
        elif line.startswith("Recommendation"):
            current_section = "Recommendation"
        elif line.startswith("Confidence Level"):
            current_section = "Confidence Level"
        elif line.startswith("Next Best Action"):
            current_section = "Next Best Action"
        elif current_section:
            sections[current_section] += line + " "

    return sections


if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Ask a Business Question")
    user_question = st.text_input("Example: Which segment should we focus on for growth?")

    if st.button("Generate Decision Insight", type="primary"):
        if user_question:
            with st.spinner("Analyzing data..."):
                preview_text = df.head(20).to_string()
                result = ask_ai(user_question, preview_text)
                parsed = parse_response(result)

            st.success("AI analysis completed")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📊 Key Insight")
                st.write(parsed["Key Insight"])

                st.markdown("### 💼 Business Implication")
                st.write(parsed["Business Implication"])

                st.markdown("### 🎯 Recommendation")
                st.write(parsed["Recommendation"])

            with col2:
                st.markdown("### 📈 Confidence Level")
                st.write(parsed["Confidence Level"])

                st.markdown("### ⚡ Next Best Action")
                st.write(parsed["Next Best Action"])

        else:
            st.warning("Please enter a question.")
else:
    st.info("Upload a dataset to begin.")
