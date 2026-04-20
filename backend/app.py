import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Load Model
# -------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------------------
# Decision Intelligence Functions
# -------------------------------

def classify_question(query):
    query = query.lower()

    if "why" in query or "reason" in query or "cause" in query:
        return "Diagnostic"
    elif "should" in query or "recommend" in query or "best action" in query or "what to do" in query:
        return "Prescriptive"
    elif "what" in query or "how many" in query or "which" in query or "show" in query:
        return "Descriptive"
    else:
        return "General"


def get_confidence_label(similarity_score):
    if similarity_score >= 0.80:
        return "High"
    elif similarity_score >= 0.60:
        return "Medium"
    else:
        return "Low"


def generate_recommended_action(question_type):
    if question_type == "Diagnostic":
        return "Investigate the root cause across product, region, or customer segment."
    elif question_type == "Prescriptive":
        return "Prioritize high-impact actions based on current performance trends."
    elif question_type == "Descriptive":
        return "Use this insight to guide deeper analysis or decision-making."
    else:
        return "Review this insight and decide next business steps accordingly."


def generate_business_impact(question_type):
    if question_type == "Diagnostic":
        return "Helps identify and fix performance gaps quickly."
    elif question_type == "Prescriptive":
        return "Supports faster and more confident decision-making."
    elif question_type == "Descriptive":
        return "Improves visibility into business performance."
    else:
        return "Supports better business awareness."

# -------------------------------
# Streamlit UI
# -------------------------------

st.title("AI Sales Decision Copilot")

# Upload dataset
uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.write(df.head())

    st.write("Columns in dataset:", df.columns)

    # Assume first column = questions, second = answers (adjust if needed)
    question_col = df.columns[0]
    answer_col = df.columns[1]

    questions = df[question_col].astype(str).tolist()
    answers = df[answer_col].astype(str).tolist()

    # Encode questions
    question_embeddings = model.encode(questions)

    # User input
    user_query = st.text_input("Ask a business question")

    st.markdown("### Try example questions:")
    st.markdown("- Why did sales drop last quarter?")
    st.markdown("- Which product is underperforming?")
    st.markdown("- What should we do to improve revenue?")

    if user_query:
        # Encode query
        query_embedding = model.encode([user_query])

        # Similarity
        similarities = cosine_similarity(query_embedding, question_embeddings)[0]
        best_idx = similarities.argmax()
        best_score = similarities[best_idx]

        matched_question = questions[best_idx]
        matched_answer = answers[best_idx]

        # Decision logic
        question_type = classify_question(user_query)
        confidence_label = get_confidence_label(best_score)
        recommended_action = generate_recommended_action(question_type)
        business_impact = generate_business_impact(question_type)

        # Output
        if best_score < 0.50:
            st.error("Low confidence result. Please rephrase your question.")
        else:
            st.markdown("## Decision Summary")

            st.markdown(f"*Matched Question:* {matched_question}")
            st.markdown(f"*Answer:* {matched_answer}")
            st.markdown(f"*Question Type:* {question_type}")
            st.markdown(f"*Confidence Score:* {best_score:.2f}")

            if confidence_label == "High":
                st.success(f"Confidence Level: {confidence_label}")
            elif confidence_label == "Medium":
                st.warning(f"Confidence Level: {confidence_label}")
            else:
                st.error(f"Confidence Level: {confidence_label}")

            st.markdown("## Recommended Action")
            st.markdown(recommended_action)

            st.markdown("## Business Impact")
            st.markdown(business_impact)
