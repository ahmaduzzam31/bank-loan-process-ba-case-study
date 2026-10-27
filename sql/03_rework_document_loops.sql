-- Rework: impact of "missing documents" loops on time to decision and withdrawal.
WITH loops AS (
    SELECT case_id, COUNT(*) FILTER (WHERE activity = 'Missing documents requested') AS doc_requests
    FROM event_log GROUP BY case_id
),
timing AS (
    SELECT
        case_id,
        MIN(timestamp) FILTER (WHERE activity = 'Application submitted') AS submitted,
        MIN(timestamp) FILTER (WHERE activity IN ('Credit committee decision', 'Delegated authority decision')) AS decided
    FROM event_log GROUP BY case_id
)
SELECT
    CASE WHEN l.doc_requests >= 3 THEN '3+' ELSE CAST(l.doc_requests AS VARCHAR) END AS doc_requests,
    COUNT(*)                                                                          AS applications,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)                                AS pct_of_applications,
    ROUND(MEDIAN(DATE_DIFF('hour', t.submitted, t.decided) / 24.0), 1)               AS median_days_to_decision,
    ROUND(100.0 * AVG(CASE WHEN a.outcome = 'Withdrawn' THEN 1 ELSE 0 END), 1)       AS withdrawal_rate_pct
FROM loops l
JOIN timing t USING (case_id)
JOIN applications a USING (case_id)
GROUP BY 1
ORDER BY 1;
