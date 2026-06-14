from database import run_query

query = """
SELECT *
FROM mental_health_analysis
LIMIT 5;
"""

df = run_query(query)

print(df)