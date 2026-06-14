import streamlit as st
from database import run_query

st.set_page_config(
    page_title="Mental Health AI Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Mental Health Australia AI Assistant")
st.write("Select a question or ask your own about Australian SA2 mental health prevalence.")

questions = [
    "Select a question",
    "Which regions have the highest severe prevalence?",
    "Which regions have the highest overall prevalence?",
    "What is the average mental health prevalence?",
    "Which regions have the largest affected population?",
    "Which regions are high risk?",
]

selected_question = st.selectbox("Choose a question:", questions)

custom_question = st.text_input("Or ask your own question:")

question = custom_question if custom_question else selected_question

if question and question != "Select a question":

    q = question.lower()

    if "highest severe" in q or "top severe" in q:
        query = """
        SELECT sa2_name, severe_pct, overall_pct, population
        FROM mental_health_analysis
        ORDER BY severe_pct DESC
        LIMIT 10;
        """
        df = run_query(query)

        st.subheader("Top regions by severe prevalence")
        st.dataframe(df)
        st.write("These regions show the highest severe mental health prevalence.")

    elif "highest overall" in q or "top overall" in q:
        query = """
        SELECT sa2_name, overall_pct, severe_pct, population
        FROM mental_health_analysis
        ORDER BY overall_pct DESC
        LIMIT 10;
        """
        df = run_query(query)

        st.subheader("Top regions by overall prevalence")
        st.dataframe(df)

    elif "average" in q:
        query = """
        SELECT 
            ROUND(AVG(overall_pct), 2) AS avg_overall_pct,
            ROUND(AVG(severe_pct), 2) AS avg_severe_pct,
            ROUND(AVG(mild_pct), 2) AS avg_mild_pct,
            ROUND(AVG(moderate_pct), 2) AS avg_moderate_pct
        FROM mental_health_analysis;
        """
        df = run_query(query)

        st.subheader("Average prevalence summary")
        st.dataframe(df)

    elif "largest affected" in q or "affected population" in q:
        query = """
        SELECT sa2_name, persons_with_disorder, overall_pct, severe_pct, population
        FROM mental_health_analysis
        ORDER BY persons_with_disorder DESC
        LIMIT 10;
        """
        df = run_query(query)

        st.subheader("Regions with largest affected population")
        st.dataframe(df)

    elif "high risk" in q:
        query = """
        SELECT sa2_name, overall_pct, severe_pct, population
        FROM mental_health_analysis
        WHERE overall_pct >= 25
          AND severe_pct >= 6
        ORDER BY severe_pct DESC
        LIMIT 20;
        """
        df = run_query(query)

        st.subheader("High-risk regions")
        st.dataframe(df)

    else:
        st.warning("Please choose one of the suggested questions or ask about severe, overall, average, affected population, or high-risk regions.")