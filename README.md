# 🚀 AI Sales Decision Copilot

An AI-powered backend system that transforms raw business datasets into **decision-ready insights** — not just dashboards.

---

## 📸 Project Demo

### 🔹 API Overview
![API Overview](https://raw.githubusercontent.com/kamranafridi9220-prog/ai-sales-decision-copilot/main/Screenshot%202026-04-16%20035336.png)

### 🔹 Ask Business Question
![Ask Question](https://raw.githubusercontent.com/kamranafridi9220-prog/ai-sales-decision-copilot/main/Screenshot%202026-04-16%20040140.png)

---

## 📌 Overview

Most data projects stop at visualisation.

We build dashboards.  
We track metrics.  
We observe trends.  

But when it’s time to make decisions…

We still rely on manual interpretation.

👉 This project solves that gap.

The **AI Sales Decision Copilot** allows users to:
- Upload structured datasets (CSV / Excel)
- Ask business questions in natural language
- Receive structured, decision-ready insights instantly

---

## ⚙️ Key Features

- 📊 Upload CSV/XLSX datasets  
- 🤖 Ask business questions in natural language  
- 🧠 Intelligent question matching system  
- 📈 Structured insights with:
  - Answer  
  - Insight Type  
  - Confidence Level  
- ⚡ FastAPI backend with Swagger UI  
- 🧩 Lightweight and scalable architecture  

---

## 🛠️ Tech Stack

- Python  
- FastAPI  
- Pandas  
- Uvicorn  
- OpenPyXL  
- REST API  

---

## 📁 Project Structure

backend/
 ├── main.py  
 ├── model_utils.py  
 ├── data/  
 ├── notebooks/  

---

## ⚙️ How to Run

1. Clone the repository:

git clone https://github.com/kamranafridi9220-prog/ai-sales-decision-copilot

2. Navigate to backend:

cd backend

3. Install dependencies:

pip install fastapi uvicorn pandas python-multipart openpyxl

4. Run the API:

uvicorn main:app --reload

5. Open in browser:

http://127.0.0.1:8000/docs

---

## 🧪 Example Use Case

1. Upload dataset  
2. Ask question:

Which regions have the highest business concentration?

3. Get structured response:

- Matched Question  
- Business Insight  
- Insight Type (e.g., Geographic Analysis)  
- Confidence Level  

---

## ⚠️ Challenges Faced

- Handling file uploads (CSV vs Excel parsing)  
- Designing meaningful question-matching logic  
- Working with limited dataset size  
- Structuring insights for business readability  
- Debugging API errors (500, validation issues)  

---

## 🚀 Future Improvements

- Add Machine Learning-based semantic search  
- Integrate LLM (GPT) for advanced reasoning  
- Build a frontend UI (Streamlit / Web App)  
- Enable real-time dataset connections  
- Improve scalability for large datasets  

---

## 💡 Key Insight

This project moves beyond traditional BI dashboards by introducing a **decision layer** on top of raw data.

👉 From:  
Data → Visualisation  

👉 To:  
Data → Insight → Decision  

---

## 👤 Author

Kamran Khan  
Corporate Account Executive | Business Intelligence & AI Enthusiast  

---

## 🔗 Project Link

https://github.com/kamranafridi9220-prog/ai-sales-decision-copilot
