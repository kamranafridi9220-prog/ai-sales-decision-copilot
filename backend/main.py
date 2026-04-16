from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd
from io import BytesIO
from model_utils import analyze_data, generate_insights, find_best_match

app = FastAPI(title="AI Sales Decision Copilot API")


@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(contents))
        else:
            return {"error": "Only CSV and XLSX files are supported"}

        analysis = analyze_data(df)
        insights = generate_insights(analysis)

        return {
            "filename": file.filename,
            "rows": int(df.shape[0]),
            "columns": list(df.columns),
            "analysis": analysis,
            "insights": insights
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/ask")
async def ask_question(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    try:
        contents = await file.read()

        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(contents))
        else:
            return {"error": "Only CSV and XLSX files are supported"}

        result = find_best_match(df, question)

        return {
            "your_question": question,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}