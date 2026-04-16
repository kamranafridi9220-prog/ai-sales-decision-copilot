import pandas as pd


def analyze_data(df):
    summary = {}

    try:
        summary["total_rows"] = int(df.shape[0])
        summary["total_columns"] = int(df.shape[1])

        numeric_cols = df.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0:
            summary["numeric_summary"] = df[numeric_cols].describe().to_dict()
        else:
            summary["numeric_summary"] = {}

        categorical_cols = df.select_dtypes(include=["object"]).columns
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                summary[f"top_{col}"] = df[col].value_counts().head(3).to_dict()

    except Exception as e:
        return {"error_in_analysis": str(e)}

    return summary


def generate_insights(summary):
    insights = []

    if summary.get("total_rows", 0) < 20:
        insights.append(
            "This is a relatively small dataset, so insights may be directional rather than definitive."
        )

    if summary.get("numeric_summary"):
        insights.append(
            "Numeric columns were detected, so statistical trend analysis is possible."
        )
    else:
        insights.append(
            "No numeric columns were detected; this dataset is mainly text-based or categorical."
        )

    top_keys = [key for key in summary.keys() if key.startswith("top_")]
    if top_keys:
        insights.append(
            "The dataset contains repeated categorical patterns that can support business interpretation."
        )

    if "top_Insight Type" in summary:
        insights.append(
            "Insight categories are already structured, which is useful for building a decision-support layer."
        )

    if "top_Question" in summary and summary.get("total_rows", 0) > 0:
        insights.append(
            "The data appears to be organized around business questions and answers, which is a strong base for an AI copilot workflow."
        )

    return insights


def find_best_match(df, user_question):
    try:
        if "Question" not in df.columns or "Answer" not in df.columns:
            return {
                "error": "Dataset must contain at least 'Question' and 'Answer' columns."
            }

        temp_df = df.copy()

        temp_df["Question"] = temp_df["Question"].astype(str)
        temp_df["Answer"] = temp_df["Answer"].astype(str)

        if "Insight Type" not in temp_df.columns:
            temp_df["Insight Type"] = "N/A"

        temp_df["Question_clean"] = temp_df["Question"].str.lower().str.strip()
        user_q = user_question.lower().strip()

        exact_matches = temp_df[temp_df["Question_clean"] == user_q]
        if len(exact_matches) > 0:
            row = exact_matches.iloc[0]
            return {
                "matched_question": row["Question"],
                "answer": row["Answer"],
                "insight_type": row["Insight Type"],
                "confidence": "high"
            }

        contains_matches = temp_df[
            temp_df["Question_clean"].str.contains(user_q, na=False)
        ]
        if len(contains_matches) > 0:
            row = contains_matches.iloc[0]
            return {
                "matched_question": row["Question"],
                "answer": row["Answer"],
                "insight_type": row["Insight Type"],
                "confidence": "medium"
            }

        word_matches = temp_df[
            temp_df["Question_clean"].apply(
                lambda x: any(word in x for word in user_q.split())
            )
        ]
        if len(word_matches) > 0:
            row = word_matches.iloc[0]
            return {
                "matched_question": row["Question"],
                "answer": row["Answer"],
                "insight_type": row["Insight Type"],
                "confidence": "low"
            }

        return {
            "message": "No relevant match found. Try rephrasing your question.",
            "confidence": "low"
        }

    except Exception as e:
        return {"error_in_matching": str(e)}