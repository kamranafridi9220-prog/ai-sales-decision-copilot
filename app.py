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
        padding: 58px 62px;
        border-radius: 28px;
        margin-bottom: 34px;
        color: white;
    }

    .pill {
        display: inline-block;
        padding: 8px 16px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 999px;
        margin-bottom: 22px;
        font-size: 14px;
        color: #ffffff;
    }

    .hero-title {
        font-size: 58px;
        font-weight: 850;
        line-height: 1.05;
        margin-bottom: 22px;
        max-width: 950px;
    }

    .hero-subtitle {
        font-size: 20px;
        line-height: 1.55;
        max-width: 820px;
        color: #dbeafe;
    }

    .metric-card {
        background: #f8f5ef;
        border: 1px solid #e5e0d8;
        border-radius: 24px;
        padding: 34px 28px;
        min-height: 190px;
        color: #111827;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }

    .metric-number {
        font-size: 48px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 14px;
        color: #111827;
    }

    .metric-text {
        font-size: 18px;
        line-height: 1.45;
        color: #111827;
    }

    .section-title {
        font-size: 34px;
        font-weight: 800;
        color: white;
        margin-top: 35px;
        margin-bottom: 12px;
    }

    .section-subtitle {
        color: #cbd5e1;
        font-size: 17px;
        margin-bottom: 22px;
    }

    .agent-card {
        background: #101827;
        border: 1px solid #24364f;
        border-radius: 22px;
        padding: 24px;
        min-height: 175px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.24);
    }

    .agent-title {
        font-size: 22px;
        font-weight: 750;
        color: white;
        margin-bottom: 10px;
    }

    .agent-text {
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.55;
    }

    .benefit-card {
        background: #0f172a;
        border: 1px solid #26384f;
        border-radius: 22px;
        padding: 28px;
        min-height: 190px;
        margin-bottom: 18px;
    }

    .benefit-title {
        color: white;
        font-size: 22px;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .benefit-text {
        color: #cbd5e1;
        font-size: 16px;
        line-height: 1.6;
    }

    .soft-divider {
        height: 1px;
        background: #26384f;
        margin: 34px 0;
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
            explain business implications, recommend action, and generate a practical next step.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">3x</div>
            <div class="metric-text">faster movement from raw data to business recommendation</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">5</div>
            <div class="metric-text">structured outputs: insight, implication, recommendation, confidence, action</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">1</div>
            <div class="metric-text">workflow that connects data analysis with decision-making</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">How the Decision Copilot Works</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">A simple decision-support workflow inspired by how commercial teams analyse opportunities.</div>',
    unsafe_allow_html=True
)

agent1, agent2, agent3 = st.columns(3)

with agent1:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-title">📊 Data Interpreter</div>
            <div class="agent-text">
                Reads dataset columns, sample records, and summary statistics to understand the business context behind the numbers.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with agent2:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-title">🧠 Decision Analyst</div>
            <div class="agent-text">
                Converts patterns into clear business insight, implication, confidence level, and recommendation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with agent3:
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

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

left_benefit, right_benefit = st.columns([1, 1.25])

with left_benefit:
    st.markdown(
        """
        <div class="benefit-card">
            <div class="benefit-title">The AI layer between dashboards and decisions</div>
            <div class="benefit-text">
                Traditional dashboards show what happened. This copilot helps explain what it means and what should happen next.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right_benefit:
    st.markdown(
        """
        <div class="benefit-card">
            <div class="benefit-title">Designed for sales, growth, and revenue teams</div>
            <div class="benefit-text">
                Ask questions about segments, customer opportunities, revenue gaps, follow-up priorities, or growth focus areas.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Upload Dataset</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Upload a CSV or Excel file containing sales, customer, lead, or growth data.</div>',
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
