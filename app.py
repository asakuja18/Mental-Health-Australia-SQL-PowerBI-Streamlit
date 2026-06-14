import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mental Health AI Assistant",
    page_icon="🧠",
    layout="wide"
)

@st.cache_data
def load_data():
    overall = pd.read_csv("mental_health_overall_clean_v2.csv")
    severity = pd.read_csv("mental_health_severity_clean_v2.csv")

    df = overall.merge(
        severity,
        on=["sa2_code", "sa2_name"],
        how="inner"
    )

    return df

df = load_data()

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
        result = df[["sa2_name", "severe_pct", "overall_pct", "population"]].sort_values(
            by="severe_pct", ascending=False
        ).head(10)

        st.subheader("Top regions by severe prevalence")
        st.dataframe(result)
        st.write("These regions show the highest severe mental health prevalence.")

    elif "highest overall" in q or "top overall" in q:
        result = df[["sa2_name", "overall_pct", "severe_pct", "population"]].sort_values(
            by="overall_pct", ascending=False
        ).head(10)

        st.subheader("Top regions by overall prevalence")
        st.dataframe(result)

    elif "average" in q:
        result = pd.DataFrame({
            "avg_overall_pct": [round(df["overall_pct"].mean(), 2)],
            "avg_severe_pct": [round(df["severe_pct"].mean(), 2)],
            "avg_mild_pct": [round(df["mild_pct"].mean(), 2)],
            "avg_moderate_pct": [round(df["moderate_pct"].mean(), 2)]
        })

        st.subheader("Average prevalence summary")
        st.dataframe(result)

    elif "largest affected" in q or "affected population" in q:
        result = df[["sa2_name", "persons_with_disorder", "overall_pct", "severe_pct", "population"]].sort_values(
            by="persons_with_disorder", ascending=False
        ).head(10)

        st.subheader("Regions with largest affected population")
        st.dataframe(result)

    elif "high risk" in q:
        result = df[
            (df["overall_pct"] >= 25) &
            (df["severe_pct"] >= 6)
        ][["sa2_name", "overall_pct", "severe_pct", "population"]].sort_values(
            by="severe_pct", ascending=False
        ).head(20)

        st.subheader("High-risk regions")
        st.dataframe(result)

    else:
        st.warning("Please choose one of the suggested questions.")
