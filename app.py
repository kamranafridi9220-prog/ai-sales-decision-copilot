import os
import pandas as pd
import streamlit as st
import plotly.express as px
from openai import OpenAI

st.set_page_config(
    page_title="AI Sales Decision Copilot",
    page_icon="📊",
    layout="wide"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown(
    """
    <style>
    .stApp {
        background-color: #020617;
        color: #f8fafc;
    }

    .hero {
        background: linear-gradient(135deg, #020617 0%, #0f172a 55%, #1e3a8a 100%);
        padding: 48px 55px;
        border-radius: 26px;
        margin-bottom: 28px;
        border: 1px solid #1e293b;
    }

    .pill {
        display: inline-block;
        padding: 8px 16px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 999px;
        margin-bottom: 18px;
        font-size: 13px;
        color: #cbd5e1;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 850;
        line-height: 1.05;
        margin-bottom: 18px;
        color: #f8fafc;
    }

    .hero-subtitle {
        font-size: 18px;
        line-height: 1.6;
        max-width: 850px;
        color: #cbd5e1;
    }

    .metric-card {
        background: #0b1220;
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.35);
    }

    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #f8fafc;
    }

    .section-title {
        font-size: 30px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 28px;
        margin-bottom: 10px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 20px;
    }

    .insight-card {
        background: #0b1220;
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 16px;
    }

    .soft-divider {
        height: 1px;
        background: #1e293b;
        margin: 30px 0;
    }

    section[data-testid="stFileUploader"] {
        background-color: #0b1220;
        border: 1px solid #1e293b;
        padding: 18px;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <div class="pill">AI-Powered Business Performance Dashboard</div>
        <div class="hero-title">Turn uploaded sales data into KPIs, charts, and decisions.</div>
        <div class="hero-subtitle">
            Upload a CSV or Excel file, explore performance metrics, visualise revenue, cost and profit,
            then ask AI business questions to generate decision-ready recommendations.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your business dataset",
    type=["csv", "xlsx"]
)


def clean_column_names(df):
    df.columns = [str(col).strip() for col in df.columns]
    return df


def find_column(df, possible_names):
    lower_columns = {col.lower(): col for col in df.columns}
    for name in possible_names:
        if name.lower() in lower_columns:
            return lower_columns[name.lower()]
    return None


def format_currency(value):
    try:
        return f"£{value:,.0f}"
    except Exception:
        return "£0"


def format_percent(value):
    try:
        return f"{value:.1f}%"
    except Exception:
        return "0%"


def ask_ai(question, data_context):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a senior business performance analyst. Give structured, practical, decision-ready insights."
            },
            {
                "role": "user",
                "content": f"""
You are analysing a business performance dataset.

Dataset context:
{data_context}

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
            sections[current_section] += line.replace("Key Insight:", "").strip() + " "
        elif line.startswith("Business Implication"):
            current_section = "Business Implication"
            sections[current_section] += line.replace("Business Implication:", "").strip() + " "
        elif line.startswith("Recommendation"):
            current_section = "Recommendation"
            sections[current_section] += line.replace("Recommendation:", "").strip() + " "
        elif line.startswith("Confidence Level"):
            current_section = "Confidence Level"
            sections[current_section] += line.replace("Confidence Level:", "").strip() + " "
        elif line.startswith("Next Best Action"):
            current_section = "Next Best Action"
            sections[current_section] += line.replace("Next Best Action:", "").strip() + " "
        elif current_section:
            sections[current_section] += line + " "

    return sections


def build_report(parsed, question, total_revenue, total_cost, total_profit, margin):
    return f"""
AI Sales Decision Copilot Report

Business Question:
{question}

Dashboard KPIs:
Total Revenue: {format_currency(total_revenue)}
Total Cost: {format_currency(total_cost)}
Total Profit: {format_currency(total_profit)}
Profit Margin: {format_percent(margin)}

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

    df = clean_column_names(df)

    st.success("Dataset uploaded successfully.")

    revenue_col = find_column(df, ["Revenue", "Sales", "Total Sales", "Amount", "Income"])
    cost_col = find_column(df, ["Cost", "Costs", "Expense", "Expenses", "Total Cost"])
    profit_col = find_column(df, ["Profit", "Gross Profit", "Net Profit", "Margin Value"])
    date_col = find_column(df, ["Date", "Order Date", "Month", "Transaction Date"])
    segment_col = find_column(df, ["Segment", "Customer Segment", "Industry", "Category"])
    region_col = find_column(df, ["Region", "Location", "Area", "Country", "City"])
    product_col = find_column(df, ["Product", "Product Name", "Service", "Item"])
    customer_col = find_column(df, ["Customer", "Customer Name", "Client", "Company Name"])

    if revenue_col:
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce").fillna(0)

    if cost_col:
        df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce").fillna(0)

    if profit_col:
        df[profit_col] = pd.to_numeric(df[profit_col], errors="coerce").fillna(0)

    if not profit_col and revenue_col and cost_col:
        df["Calculated Profit"] = df[revenue_col] - df[cost_col]
        profit_col = "Calculated Profit"

    st.markdown('<div class="section-title">Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    total_revenue = df[revenue_col].sum() if revenue_col else 0
    total_cost = df[cost_col].sum() if cost_col else 0
    total_profit = df[profit_col].sum() if profit_col else 0
    margin = (total_profit / total_revenue * 100) if total_revenue else 0
    total_rows = len(df)
    unique_customers = df[customer_col].nunique() if customer_col else total_rows

    st.markdown('<div class="section-title">Business Performance Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Automatically generated KPIs from your uploaded dataset.</div>',
        unsafe_allow_html=True
    )

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    with kpi1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Revenue</div>
                <div class="metric-value">{format_currency(total_revenue)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Cost</div>
                <div class="metric-value">{format_currency(total_cost)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Profit</div>
                <div class="metric-value">{format_currency(total_profit)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Profit Margin</div>
                <div class="metric-value">{format_percent(margin)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi5:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Records</div>
                <div class="metric-value">{total_rows:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Visual Performance Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Charts change automatically based on available columns in your file.</div>',
        unsafe_allow_html=True
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if segment_col and revenue_col:
            segment_revenue = df.groupby(segment_col, as_index=False)[revenue_col].sum()
            fig = px.bar(
                segment_revenue,
                x=segment_col,
                y=revenue_col,
                title="Revenue by Segment / Category",
                text_auto=True
            )
            fig.update_layout(
                paper_bgcolor="#020617",
                plot_bgcolor="#020617",
                font_color="#f8fafc"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add a Segment/Category and Revenue column to show revenue by segment.")

    with chart_col2:
        if segment_col and profit_col:
            segment_profit = df.groupby(segment_col, as_index=False)[profit_col].sum()
            fig = px.pie(
                segment_profit,
                names=segment_col,
                values=profit_col,
                title="Profit Share by Segment / Category"
            )
            fig.update_layout(
                paper_bgcolor="#020617",
                plot_bgcolor="#020617",
                font_color="#f8fafc"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add a Segment/Category and Profit column to show profit share.")

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        if region_col and revenue_col:
            region_revenue = df.groupby(region_col, as_index=False)[revenue_col].sum()
            fig = px.bar(
                region_revenue,
                x=region_col,
                y=revenue_col,
                title="Revenue by Region / Location",
                text_auto=True
            )
            fig.update_layout(
                paper_bgcolor="#020617",
                plot_bgcolor="#020617",
                font_color="#f8fafc"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add a Region/Location and Revenue column to show regional performance.")

    with chart_col4:
        if product_col and profit_col:
            product_profit = (
                df.groupby(product_col, as_index=False)[profit_col]
                .sum()
                .sort_values(by=profit_col, ascending=False)
                .head(10)
            )
            fig = px.bar(
                product_profit,
                x=product_col,
                y=profit_col,
                title="Top Products / Services by Profit",
                text_auto=True
            )
            fig.update_layout(
                paper_bgcolor="#020617",
                plot_bgcolor="#020617",
                font_color="#f8fafc"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add a Product/Service and Profit column to show product performance.")

    if date_col and revenue_col:
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            trend_df = (
                df.dropna(subset=[date_col])
                .groupby(date_col, as_index=False)[revenue_col]
                .sum()
                .sort_values(by=date_col)
            )

            fig = px.line(
                trend_df,
                x=date_col,
                y=revenue_col,
                title="Revenue Trend Over Time",
                markers=True
            )
            fig.update_layout(
                paper_bgcolor="#020617",
                plot_bgcolor="#020617",
                font_color="#f8fafc"
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception:
            st.info("Date column found, but could not generate time trend.")

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Ask AI About This Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Ask questions and the AI will use the dataset summary, KPIs, and sample data to produce decision-ready answers.</div>',
        unsafe_allow_html=True
    )

    sample_questions = [
        "Which segment should we focus on for growth?",
        "Where are we losing revenue opportunities?",
        "Which product or service is most profitable?",
        "What should we do next to improve margin?",
        "Which region needs more attention?"
    ]

    selected_question = st.selectbox(
        "Choose a sample question or type your own below:",
        sample_questions
    )

    user_question = st.text_input(
        "Business question",
        value=selected_question
    )

    if st.button("Generate AI Decision Insight", type="primary"):
        if user_question:
            with st.spinner("AI decision copilot is analysing your dashboard..."):
                data_context = f"""
Columns:
{', '.join(df.columns)}

Detected Columns:
Revenue Column: {revenue_col}
Cost Column: {cost_col}
Profit Column: {profit_col}
Date Column: {date_col}
Segment Column: {segment_col}
Region Column: {region_col}
Product Column: {product_col}
Customer Column: {customer_col}

KPIs:
Total Revenue: {total_revenue}
Total Cost: {total_cost}
Total Profit: {total_profit}
Profit Margin: {margin}
Total Records: {total_rows}
Unique Customers: {unique_customers}

Dataset Summary:
{df.describe(include='all').to_string()}

Sample Data:
{df.head(10).to_string()}
"""
                result = ask_ai(user_question, data_context)
                parsed = parse_response(result)

            st.success("Decision insight generated.")

            tab1, tab2 = st.tabs(["📊 AI Decision Output", "📥 Download Report"])

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
                report_text = build_report(
                    parsed,
                    user_question,
                    total_revenue,
                    total_cost,
                    total_profit,
                    margin
                )

                st.download_button(
                    label="📥 Download Full Decision Report",
                    data=report_text,
                    file_name="ai_sales_dashboard_decision_report.txt",
                    mime="text/plain"
                )

        else:
            st.warning("Please enter a business question.")

else:
    st.markdown(
        """
        <div style='background:#0f2a44;padding:14px;border-radius:12px;color:#cbd5e1;border:1px solid #1e40af;'>
            Upload a dataset to begin.
        </div>
        """,
        unsafe_allow_html=True
    )
