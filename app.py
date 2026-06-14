import requests
import streamlit as st
from database import run_query

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

st.set_page_config(
    page_title="Mental Health Australia AI Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Mental Health Australia AI Assistant")
st.write("Ask any question about Australian SA2 mental health prevalence.")

SCHEMA = """
Table: mental_health_analysis

Columns:
- sa2_code
- sa2_name
- persons_with_disorder
- overall_pct
- mild_pct
- moderate_pct
- severe_pct
- population

Business definitions:
- affected population means persons_with_disorder
- overall prevalence means overall_pct
- severe prevalence means severe_pct
- mild prevalence means mild_pct
- moderate prevalence means moderate_pct
- region means sa2_name
"""

def ask_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["response"].strip()


def generate_sql(user_question):
    prompt = f"""
You are a PostgreSQL SQL assistant.

Use only this table and columns:

{SCHEMA}

Rules:
- Generate only one SELECT query.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE.
- Always use the table mental_health_analysis.
- Always limit results to 20 rows unless the user asks for averages, totals, or counts.
- If the user asks for lowest or smallest values, sort ASC.
- If the user asks for highest or largest values, sort DESC.
- If the user says affected population, use persons_with_disorder.
- Return SQL only. No explanation. No markdown.

User question:
{user_question}
"""

    sql = ask_ollama(prompt)

    sql = (
        sql.replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    return sql


def is_safe_sql(sql):
    blocked_words = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate"
    ]

    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        return False

    for word in blocked_words:
        if word in sql_lower:
            return False

    return True


def generate_summary(user_question, df):
    summary_prompt = f"""
You are a healthcare data analyst.

User question:
{user_question}

Query result:
{df.head(10).to_string(index=False)}

Write a short business-style explanation in 3-4 lines.
Do not mention SQL.
Do not mention database.
Do not use technical language.
Focus on the insight and what it means.
"""

    return ask_ollama(summary_prompt)


examples = [
    "Which regions have the highest severe prevalence?",
    "Which regions have the lowest overall prevalence?",
    "Which regions have the lowest affected population?",
    "Which regions have the largest affected population?",
    "What is the average mental health prevalence?",
    "Show regions where severe prevalence is above 6%",
    "Which regions are high risk?"
]

st.caption("Example questions:")
for example in examples:
    st.write(f"• {example}")

question = st.text_input("Ask your question:")

if question:
    with st.spinner("Analysing your question..."):
        try:
            sql_query = generate_sql(question)

            if not is_safe_sql(sql_query):
                st.error("The assistant generated an unsafe or invalid query. Please rephrase your question.")
            else:
                df = run_query(sql_query)

                st.subheader("AI Summary")

                if df.empty:
                    st.warning("No matching results were found for this question.")
                else:
                    summary = generate_summary(question, df)
                    st.write(summary)

                    st.subheader("Supporting Data")
                    st.dataframe(df, use_container_width=True)

                    st.success("Answer generated using local GenAI and PostgreSQL.")

        except Exception as e:
            st.error("Something went wrong while generating the answer.")
            st.write(e)
