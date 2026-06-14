-- =====================================================
-- Mental Health Australia Analysis
-- PostgreSQL + Power BI Project
-- Data Source: ABS National Study of Mental Health
-- =====================================================

-- =====================================================
-- 1. TABLE CREATION
-- =====================================================

-- 1. Create table

CREATE TABLE mental_health_overall (
    sa2_code BIGINT,
    sa2_name TEXT,
    persons_with_disorder NUMERIC,
    rrmse_pct NUMERIC,
    flag TEXT,
    proportion_pct NUMERIC,
    lower_ci_pct NUMERIC,
    upper_ci_pct NUMERIC,
    population NUMERIC
);

CREATE TABLE mental_health_severity (
    sa2_code BIGINT,
    sa2_name TEXT,
    mild_pct NUMERIC,
    moderate_pct NUMERIC,
    severe_pct NUMERIC
);

-- =====================================================
-- 2. DATA IMPORT & VALIDATION
-- =====================================================

-- 2.1 DATA IMPORT

-- CSV files were imported into PostgreSQL using pgAdmin Import/Export.
-- Cleaned files used:
-- mental_health_overall_clean_v2.csv
-- mental_health_severity_clean_v2.csv

-- 2.2 DATA VALIDATION

Select
Count(*) 
from mental_health_overall;

Select
Count(*) 
from mental_health_severity;

SELECT * 
FROM mental_health_overall
LIMIT 10;

SELECT * 
FROM mental_health_severity
LIMIT 10;


-- =====================================================
-- 3. CREATE ANALYTICAL VIEW
-- =====================================================

CREATE OR REPLACE VIEW mental_health_analysis AS
SELECT 
    o.sa2_code,
    o.sa2_name,
    o.persons_with_disorder,
    o.proportion_pct AS overall_pct,
    s.mild_pct,
    s.moderate_pct,
    s.severe_pct,
    o.population
FROM mental_health_overall o
JOIN mental_health_severity s
ON o.sa2_code = s.sa2_code;

SELECT * 
FROM mental_health_analysis
LIMIT 10;

-- =====================================================
-- 4. BASIC SQL ANALYSIS
-- =====================================================

-- 4.1 Top 10 SA2 regions with highest severe mental disorder prevalence

SELECT 
    sa2_name,
    overall_pct,
    mild_pct,
    moderate_pct,
    severe_pct,
    population
FROM mental_health_analysis
ORDER BY severe_pct DESC
LIMIT 10;

-- 4.2 Top 10 SA2 regions with highest overall mental disorder prevalence

SELECT 
    sa2_name,
    overall_pct,
    population
FROM mental_health_analysis
ORDER BY overall_pct DESC
LIMIT 10;

-- 4.3 Lowest overall prevalence, excluding very small population areas

SELECT
    sa2_name,
    overall_pct,
    population
FROM mental_health_analysis
WHERE population > 1000
ORDER BY overall_pct ASC
LIMIT 10;


-- 4.4 High-risk SA2 regions with both high overall and severe prevalence

SELECT 
    sa2_name,
    overall_pct,
    severe_pct,
    population
FROM mental_health_analysis
WHERE overall_pct > 25
  AND severe_pct > 6
ORDER BY severe_pct DESC;

-- 4.5 Average prevalence by severity level across Australia

SELECT 
    ROUND(AVG(mild_pct), 2) AS avg_mild_pct,
    ROUND(AVG(moderate_pct), 2) AS avg_moderate_pct,
    ROUND(AVG(severe_pct), 2) AS avg_severe_pct
FROM mental_health_analysis;


-- =====================================================
-- 5. ADVANCED SQL ANALYSIS
-- =====================================================

-- 5.1 Rank SA2 regions by severe mental disorder prevalence

SELECT
    sa2_name,
    overall_pct,
    severe_pct,
    RANK() OVER (ORDER BY severe_pct DESC) AS severe_rank
FROM mental_health_analysis
WHERE population > 1000
ORDER BY severe_rank
LIMIT 20;


-- 5.2 Compare each SA2's prevalence against the national average

WITH national_avg AS (
    SELECT AVG(overall_pct) AS avg_overall_pct
    FROM mental_health_analysis
    WHERE population > 1000
)
SELECT
    m.sa2_name,
    m.overall_pct,
    ROUND(n.avg_overall_pct, 2) AS national_avg_pct,
    ROUND(m.overall_pct - n.avg_overall_pct, 2) AS difference_from_avg
FROM mental_health_analysis m
CROSS JOIN national_avg n
WHERE m.population > 1000
ORDER BY difference_from_avg DESC
LIMIT 20;


-- 5.3 Create a custom severity risk score for each SA2 region

SELECT
    sa2_name,
    overall_pct,
    mild_pct,
    moderate_pct,
    severe_pct,
    ROUND(
        (mild_pct * 1) +
        (moderate_pct * 2) +
        (severe_pct * 3), 2
    ) AS severity_risk_score
FROM mental_health_analysis
WHERE population > 1000
ORDER BY severity_risk_score DESC
LIMIT 20;

-- 5.4 Assign percentile ranking based on overall mental disorder prevalence

SELECT
    sa2_name,
    overall_pct,
    population,
    ROUND(
        PERCENT_RANK() OVER (ORDER BY overall_pct)::numeric, 3
    ) AS prevalence_percentile
FROM mental_health_analysis
WHERE population > 1000
ORDER BY prevalence_percentile DESC
LIMIT 20;

-- 5.5 Classify SA2 regions into Low, Medium, High, and Very High risk groups

SELECT
    sa2_name,
    overall_pct,
    severe_pct,
    population,
    CASE
        WHEN overall_pct >= 30 OR severe_pct >= 8 THEN 'Very High Risk'
        WHEN overall_pct >= 25 OR severe_pct >= 6 THEN 'High Risk'
        WHEN overall_pct >= 20 OR severe_pct >= 4 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM mental_health_analysis
WHERE population > 1000
ORDER BY overall_pct DESC;

-- 5.6 Count how many SA2 regions fall into each risk category

WITH risk_classification AS (
    SELECT
        sa2_name,
        CASE
            WHEN overall_pct >= 30 OR severe_pct >= 8 THEN 'Very High Risk'
            WHEN overall_pct >= 25 OR severe_pct >= 6 THEN 'High Risk'
            WHEN overall_pct >= 20 OR severe_pct >= 4 THEN 'Medium Risk'
            ELSE 'Low Risk'
        END AS risk_category
    FROM mental_health_analysis
    WHERE population > 1000
)
SELECT
    risk_category,
    COUNT(*) AS number_of_regions
FROM risk_classification
GROUP BY risk_category
ORDER BY number_of_regions DESC;


-- 5.7 Calculate severe prevalence as a share of total mental disorder prevalence

SELECT
    sa2_name,
    overall_pct,
    severe_pct,
    ROUND((severe_pct / NULLIF(overall_pct, 0)) * 100, 2) AS severe_share_of_total_pct
FROM mental_health_analysis
WHERE population > 1000
ORDER BY severe_share_of_total_pct DESC
LIMIT 20;

-- 5.8 Calculate population-weighted national mental disorder prevalence

SELECT
    ROUND(
        SUM(overall_pct * population) / SUM(population), 2
    ) AS population_weighted_overall_prevalence
FROM mental_health_analysis
WHERE population > 1000;