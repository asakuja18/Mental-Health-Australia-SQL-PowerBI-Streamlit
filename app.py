import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mental Health Australia AI Assistant",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
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

# -----------------------------
# Header
# -----------------------------
st.title("🧠 Mental Health Australia AI Assistant")

st.write(
    "Select a question or ask your own about Australian SA2 mental health prevalence."
)

# -----------------------------
# Suggested Questions
# -----------------------------
questions = [
    "Select a question",
    "Which regions have the highest severe prevalence?",
    "Which regions have the lowest severe prevalence?",
    "Which regions have the highest overall prevalence?",
    "What is the average mental health prevalence?",
    "Which regions have the largest affected population?",
    "Which regions are high risk?"
]

selected_question = st.selectbox(
    "Choose a question:",
    questions
)

custom_question = st.text_input(
    "Or ask your own question:"
)

question = custom_question if custom_question else selected_question

# -----------------------------
# Question Logic
# -----------------------------
if question and question != "Select a question":

    q = (
        question.lower()
        .replace("prevalance", "prevalence")
        .replace("highest", "top")
    )

    # ---------------------------------
    # Highest Severe Prevalence
    # ---------------------------------
    if (
        "top severe" in q
        or "highest severe" in q
        or "severe prevalence" in q
    ):

        result = (
            df[
                [
                    "sa2_name",
                    "severe_pct",
                    "overall_pct",
                    "population"
                ]
            ]
            .sort_values(
                by="severe_pct",
                ascending=False
            )
            .head(10)
        )

        st.subheader("Top Regions by Severe Prevalence")

        st.dataframe(
            result,
            use_container_width=True
        )

        st.success(
            "These regions show the highest severe mental health prevalence."
        )

    # ---------------------------------
    # Lowest Severe Prevalence
    # ---------------------------------
    elif (
        "lowest severe" in q
        or "low severe" in q
        or "least severe" in q
    ):

        result = (
            df[
                [
                    "sa2_name",
                    "severe_pct",
                    "overall_pct",
                    "population"
                ]
            ]
            .sort_values(
                by="severe_pct",
                ascending=True
            )
            .head(10)
        )

        st.subheader("Regions with Lowest Severe Prevalence")

        st.dataframe(
            result,
            use_container_width=True
        )

        st.success(
            "These regions have the lowest severe mental health prevalence."
        )

    # ---------------------------------
    # Highest Overall Prevalence
    # ---------------------------------
    elif (
        "overall" in q
        or "highest prevalence" in q
        or "top prevalence" in q
    ):

        result = (
            df[
                [
                    "sa2_name",
                    "overall_pct",
                    "severe_pct",
                    "population"
                ]
            ]
            .sort_values(
                by="overall_pct",
                ascending=False
            )
            .head(10)
        )

        st.subheader("Top Regions by Overall Prevalence")

        st.dataframe(
            result,
            use_container_width=True
        )

        st.success(
            "These regions show the highest overall mental health prevalence."
        )

    # ---------------------------------
    # Average Prevalence
    # ---------------------------------
    elif "average" in q:

        result = pd.DataFrame({
            "Average Overall %":
                [round(df["overall_pct"].mean(), 2)],
            "Average Mild %":
                [round(df["mild_pct"].mean(), 2)],
            "Average Moderate %":
                [round(df["moderate_pct"].mean(), 2)],
            "Average Severe %":
                [round(df["severe_pct"].mean(), 2)]
        })

        st.subheader("Average Mental Health Prevalence")

        st.dataframe(
            result,
            use_container_width=True
        )

    # ---------------------------------
    # Largest Affected Population
    # ---------------------------------
    elif (
        "affected population" in q
        or "largest affected" in q
        or "persons with disorder" in q
    ):

        result = (
            df[
                [
                    "sa2_name",
                    "persons_with_disorder",
                    "overall_pct",
                    "population"
                ]
            ]
            .sort_values(
                by="persons_with_disorder",
                ascending=False
            )
            .head(10)
        )

        st.subheader("Largest Affected Population")

        st.dataframe(
            result,
            use_container_width=True
        )

        st.success(
            "These regions contain the largest number of people with mental health conditions."
        )

    # ---------------------------------
    # High Risk Regions
    # ---------------------------------
    elif "high risk" in q:

        result = (
            df[
                (df["overall_pct"] >= 25)
                & (df["severe_pct"] >= 6)
            ][
                [
                    "sa2_name",
                    "overall_pct",
                    "severe_pct",
                    "population"
                ]
            ]
            .sort_values(
                by="severe_pct",
                ascending=False
            )
            .head(20)
        )

        st.subheader("High Risk Regions")

        st.dataframe(
            result,
            use_container_width=True
        )

        st.success(
            "These regions exceed the defined high-risk thresholds."
        )

    # ---------------------------------
    # Fallback
    # ---------------------------------
    else:

        st.warning(
            "Please choose one of the suggested questions."
        )
