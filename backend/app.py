import streamlit as st
import pandas as pd
from model_utils import find_best_match

st.set_page_config(page_title="AI Sales Decision Copilot", layout="wide")

st.title("AI Sales Decision Copilot")
st.write("Upload a business dataset, analyze it, and ask a business question.")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully")

        # Show preview
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        # Ask question
        st.subheader("Ask a Business Question")
        question = st.text_input("Enter your question")

        if st.button("Get Answer"):
            if question.strip():
                result = find_best_match(df, question)

                st.subheader("Result")
                st.write(f"**Matched Question:** {result.get('matched_question')}")
                st.write(f"**Answer:** {result.get('answer')}")
                st.write(f"**Insight Type:** {result.get('insight_type')}")
                st.write(f"**Confidence:** {result.get('confidence')}")
            else:
                st.warning("Please enter a question.")

    except Exception as e:
        st.error(f"Error: {e}")