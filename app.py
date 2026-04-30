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

st.markdown(
    """
    <style>
    .main {
        background-color: #07111f;
    }

    .hero {
        background: linear-gradient(135deg, #061a40 0%, #0b3d91 55%, #0f62fe 100%);
        padding: 55px 60px;
        border-radius: 26px;
        margin-bottom: 35px;
        color: white;
    }

    .hero-title {
        font-size: 56px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 22px;
    }

    .hero-subtitle {
        font-size: 20px;
        line-height: 1.5;
        max-width: 780px;
        color: #dbeafe;
    }

    .pill {
        display: inline-block;
        padding: 8px 15px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 999px;
        margin-bottom: 22px;
        font-size: 14px;
        color: #ffffff;
    }

    .agent-card {
        background: #101827;
        border: 1px solid #24364f;
        border-radius: 20px;
        padding: 24px;
        min-height: 170px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }

    .agent-title {
        font-size: 22px;
        font-weight: 700;
        color: white;
        margin-bottom: 8px;
    }

    .agent-text {
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.5;
    }

    .section-title {
        font-size: 34px;
        font-weight: 800;
        color: white;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .section-subtitle {
        color: #cbd5e1;
        font-size: 17px;
        margin-bottom: 22px;
    }

    .result-card {
        background: #0f172a;
        border: 1px solid #26384f;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .small-muted {
        color: #94a3b8;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <div class="pill">AI Decision System for Sales Teams</div>
        <div class="hero-title">Turn sales data into decisions — not just dashboards.</div>
        <div class="hero-subtitle">
            Upload a dataset, ask a business question, and let an AI decision copilot analyse patterns,
            explain implications, recommend action, and generate a practical next step.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-title">📊 Data Interpreter</div>
            <div class="agent-text">
                Reads the uploaded dataset structure, column patterns, and sample records to understand the business context.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_b:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-title">🧠 Decision Analyst</div>
            <div class="agent-text">
                Converts raw data into key insights, implications, confidence levels, and decision-ready recommendations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_c:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-title">⚡ Action Planner</div>
            <div class="agent-text">
                Suggests the next best action so teams can move from analysis to execution faster.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

st.markdown('<div class="section-title">Upload Dataset</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Upload a CSV or Excel file containing sales, customer, or lead data.</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])


def ask_ai(question, data_preview):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a senior business decision analyst. Always respond in clearly separated sections."
            },
            {
                "role": "user",
                "content": f"""
You are analyzing a real business dataset.

Dataset context:
{data_preview}

Business question:
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


def build_report(parsed, question):
    return f"""
AI Sales Decision Copilot Report

Business Question:
{question}

Key Insight:
{parsed['Key Insight']}

Business Implication:
{parsed['Business Implication']}

Recommendation:
{parsed['Recommendation']}

Confidence Level:
{parsed['Confidence Level']}

Next Best Action:
{parsed['Next Best Action']}
"""


if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Dataset uploaded successfully.")

    st.markdown('<div class="section-title">Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    st.markdown('<div class="section-title">Ask a Business Question</div>', unsafe_allow_html=True)
    st.caption("Try: Which segment should we focus on for growth? OR Where are we losing revenue opportunities?")

    user_question = st.text_input(
        "Business question",
        placeholder="Example: Which segment should we focus on for growth?"
    )

    if st.button("Generate Decision Insight", type="primary"):
        if user_question:
            with st.spinner("AI decision copilot is analysing the dataset..."):
                data_context = f"""
Columns:
{', '.join(df.columns)}

Dataset Summary:
{df.describe(include='all').to_string()}

Sample Data:
{df.head(10).to_string()}
"""
                result = ask_ai(user_question, data_context)
                parsed = parse_response(result)

            st.success("Decision insight generated.")

            tab1, tab2 = st.tabs(["📊 Decision Output", "📥 Download Report"])

            with tab1:
                left, right = st.columns(2)

                with left:
                    st.markdown("### 📊 Key Insight")
                    st.write(parsed["Key Insight"])

                    st.markdown("### 💼 Business Implication")
                    st.write(parsed["Business Implication"])

                    st.markdown("### 🎯 Recommendation")
                    st.write(parsed["Recommendation"])

                with right:
                    st.markdown("### 📈 Confidence Level")
                    confidence = parsed["Confidence Level"].lower()

                    if "high" in confidence:
                        st.success(parsed["Confidence Level"])
                    elif "medium" in confidence:
                        st.warning(parsed["Confidence Level"])
                    else:
                        st.error(parsed["Confidence Level"])

                    st.markdown("### ⚡ Next Best Action")
                    st.write(parsed["Next Best Action"])

            with tab2:
                report_text = build_report(parsed, user_question)

                st.download_button(
                    label="📥 Download Full Decision Report",
                    data=report_text,
                    file_name="ai_sales_decision_report.txt",
                    mime="text/plain"
                )

        else:
            st.warning("Please enter a business question.")

else:
    st.info("Upload a dataset to begin.")
