# Mental Health Treatment Gap Analysis Australia

Built an AI-powered Mental Health Analytics Platform using PostgreSQL, SQL, Power BI, Python, Streamlit, and local LLMs (Ollama) to enable natural-language exploration of Australian mental health data.

## Dashboard Preview

<img width="850" height="476" alt="Screenshot 2026-06-14 at 4 00 10 PM" src="https://github.com/user-attachments/assets/a0a3bccc-bdd4-4775-bf81-f9dc95ad5215" />
An interactive Power BI dashboard providing regional mental health analysis, severity distribution, prevalence benchmarking, and high-risk region identification across Australian SA2 regions.

## AI Assistant Preview

<img width="1440" height="900" alt="Screenshot 2026-06-14 at 7 57 19 PM" src="https://github.com/user-attachments/assets/ab620400-50bf-4039-8f6b-23334467d220" />

AI Assistant home screen with predefined and custom question options.

## AI Query Example


<img width="1440" height="900" alt="Screenshot 2026-06-14 at 7 56 32 PM" src="https://github.com/user-attachments/assets/4d4d4849-49d3-4299-8442-d8b6df3a2520" />

<img width="1440" height="900" alt="Screenshot 2026-06-14 at 7 57 54 PM" src="https://github.com/user-attachments/assets/7777b4b7-b49d-45bd-aed8-e6fbf1c7439e" />



---
## Tech Stack

- PostgreSQL
- SQL
- Power BI
- Python
- Streamlit
- Pandas

---

## Project Overview

Mental health remains one of Australia's most significant public health challenges, yet access to treatment and support varies considerably across regions. Understanding where mental health prevalence is highest can help governments, healthcare providers, and policymakers prioritise resources and interventions more effectively.

This project explores mental health prevalence across Australian SA2 regions using a combination of SQL analytics, Power BI visualisation, and an AI-powered assistant for interactive exploration.

---

## Business Problem

Mental health prevalence data is often spread across multiple datasets and difficult for non-technical stakeholders to analyse. Decision-makers require a clear view of:

* Which regions experience the highest mental health burden.
* The distribution of mild, moderate, and severe conditions.
* Areas that exceed national prevalence targets.
* Regions that may require additional support and intervention.

The objective was to transform raw statistical data into an interactive decision-support solution.

---

## Solution

To address this challenge, a PostgreSQL analytical database was developed and integrated with Power BI to create an interactive dashboard for exploring regional mental health trends.

The dashboard allows users to:

* Analyse mental health prevalence across Australian SA2 regions.
* Compare severity levels across locations.
* Identify high-risk regions.
* Monitor prevalence against national targets.
* Filter results dynamically using regional selections.

To further enhance accessibility, a lightweight AI assistant was developed using Python and Streamlit. The assistant enables users to ask predefined analytical questions and retrieve insights from the underlying database instantly.

---

## Project Architecture

CSV Data Sources
→ PostgreSQL Database
→ SQL Analysis & Views
→ Power BI Dashboard
→ Streamlit AI Assistant

---

## Key Insights

Analysis revealed substantial variation in mental health prevalence across Australian regions, with several areas displaying significantly higher severe prevalence rates than the national target.

The project demonstrates how data analytics and conversational AI can be combined to support evidence-based decision-making in public health.

---

## Project Outcome

This project delivers an end-to-end analytics solution that combines data engineering, SQL analysis, business intelligence reporting, and AI-assisted data exploration.

The result is an interactive platform that transforms complex mental health statistics into actionable insights for stakeholders and decision-makers.

---
