import requests
import streamlit as st
from database import run_query

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"   # use your installed small model

st.set_page_config(
    page_title="Mental Health Australia AI Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Mental Health Australia AI Assistant")
st.write("Ask questions about Australian SA2 mental health prevalence.")

def ask_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120
    )
    response.raise_for_status()
    return response.json()["response"].strip()

def create_query(question):
    q = question.lower().replace("prevalance", "prevalence")

    if "high risk" in q:
        return """
        SELECT sa2_name, overall_pct, severe_pct, population
        FROM mental_health_analysis
        WHERE severe_pct > 5
        ORDER BY severe_pct DESC
        LIMIT 20;
        """

    if "lowest" in q and "overall" in q:
        return """
        SELECT sa2_name, overall_pct, severe_pct, population
        FROM mental_health_analysis
        ORDER BY overall_pct ASC
        LIMIT 20;
        """

    if "highest" in q and "overall" in q:
        return """
        SELECT sa2_name, overall_pct, severe_pct, population
        FROM mental_health_analysis
        ORDER BY overall_pct DESC
        LIMIT 20;
        """

    if "lowest" in q and "severe" in q:
        return """
        SELECT sa2_name, severe_pct, overall_pct, population
        FROM mental_health_analysis
        ORDER BY severe_pct ASC
        LIMIT 20;
        """

    if "highest" in q and "severe" in q:
        return """
        SELECT sa2_name, severe_pct, overall_pct, population
        FROM mental_health_analysis
        ORDER BY severe_pct DESC
        LIMIT 20;
        """

    if "lowest" in q and ("affected" in q or "disorder" in q):
        return """
        SELECT sa2_name, persons_with_disorder, overall_pct, population
        FROM mental_health_analysis
        ORDER BY persons_with_disorder ASC
        LIMIT 20;
        """

    if "largest" in q and ("affected" in q or "disorder" in q):
        return """
        SELECT sa2_name, persons_with_disorder, overall_pct, population
        FROM mental_health_analysis
        ORDER BY persons_with_disorder DESC
        LIMIT 20;
        """

    if "average" in q:
        return """
        SELECT 
            ROUND(AVG(overall_pct), 2) AS avg_overall_pct,
            ROUND(AVG(mild_pct), 2) AS avg_mild_pct,
            ROUND(AVG(moderate_pct), 2) AS avg_moderate_pct,
            ROUND(AVG(severe_pct), 2) AS avg_severe_pct
        FROM mental_health_analysis;
        """

    if "population" in q:
        return """
        SELECT sa2_name, population, persons_with_disorder, overall_pct
        FROM mental_health_analysis
        ORDER BY population DESC
        LIMIT 20;
        """

    return None

def generate_summary(question, df):
    prompt = f"""
You are a healthcare data analyst.

User question:
{question}

Data result:
{df.head(10).to_string(index=False)}

Write a short 3-line explanation.
Do not mention SQL.
Do not mention database.
Keep it simple.
"""
    return ask_ollama(prompt)

examples = [
    "Which regions have the highest severe prevalence?",
    "Which regions have the lowest overall prevalence?",
    "Which regions have the lowest affected population?",
    "Which regions have the largest affected population?",
    "What is the average mental health prevalence?",
    "Which regions are high risk?"
]

st.caption("Example questions:")
for ex in examples:
    st.write(f"• {ex}")

question = st.text_input("Ask your question:")

if question:
    with st.spinner("Analysing your question..."):
        query = create_query(question)

        if query is None:
            st.warning("Please ask about severe prevalence, overall prevalence, affected population, average prevalence, high-risk regions, or population.")
        else:
            try:
                df = run_query(query)

                st.subheader("AI Summary")

                if df.empty:
                    st.warning("No matching results found.")
                else:
                    summary = generate_summary(question, df)
                    st.write(summary)

                    st.subheader("Supporting Data")
                    st.dataframe(df, use_container_width=True)

                    st.success("Answer generated using local GenAI and PostgreSQL.")

            except Exception as e:
                st.error("Something went wrong while retrieving the answer.")
                st.write(e)
