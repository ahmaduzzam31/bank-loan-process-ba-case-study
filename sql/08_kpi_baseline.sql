-- Baseline KPIs for the business case and future-state targets.
WITH t AS (
    SELECT
        case_id,
        MIN(timestamp) FILTER (WHERE activity = 'Application submitted') AS submitted,
        MIN(timestamp) FILTER (WHERE activity IN ('Credit committee decision', 'Delegated authority decision')) AS decided,
        MIN(timestamp) FILTER (WHERE activity = 'Loan funded') AS funded,
        COUNT(*) FILTER (WHERE activity = 'Missing documents requested') AS doc_requests
    FROM event_log GROUP BY case_id
)
SELECT
    COUNT(*)                                                                    AS applications,
    ROUND(100.0 * AVG(CASE WHEN a.outcome = 'Funded' THEN 1 ELSE 0 END), 1)    AS funded_pct,
    ROUND(100.0 * AVG(CASE WHEN a.outcome = 'Withdrawn' THEN 1 ELSE 0 END), 1) AS withdrawn_pct,
    ROUND(100.0 * AVG(CASE WHEN a.outcome = 'Declined' THEN 1 ELSE 0 END), 1)  AS declined_pct,
    ROUND(MEDIAN(DATE_DIFF('hour', submitted, decided) / 24.0), 1)             AS median_days_to_decision,
    ROUND(MEDIAN(DATE_DIFF('hour', submitted, funded) / 24.0), 1)              AS median_days_to_funding,
    ROUND(100.0 * AVG(CASE WHEN doc_requests = 0 THEN 1 ELSE 0 END), 1)        AS first_time_complete_pct,
    ROUND(100.0 * AVG(CASE WHEN DATE_DIFF('hour', submitted, decided) / 24.0 <= 7 THEN 1.0 ELSE 0 END)
          FILTER (WHERE decided IS NOT NULL), 1)                               AS decided_within_7_days_pct,
    ROUND(SUM(a.amount_eur) FILTER (WHERE a.outcome = 'Withdrawn') / 1e6, 1)   AS withdrawn_lending_eur_m
FROM t JOIN applications a USING (case_id);
