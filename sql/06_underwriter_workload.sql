-- Underwriter workload: is work evenly spread across the team?
WITH a AS (
    SELECT case_id, resource,
           MIN(timestamp) FILTER (WHERE activity = 'Credit assessment started')   AS started,
           MIN(timestamp) FILTER (WHERE activity = 'Credit assessment completed') AS completed
    FROM event_log
    WHERE role = 'Credit underwriter'
    GROUP BY case_id, resource
)
SELECT
    resource                                                         AS underwriter,
    COUNT(*)                                                         AS assessments,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)               AS share_pct,
    ROUND(100.0 * COUNT(*) / (SUM(COUNT(*)) OVER () / COUNT(*) OVER ()) - 100, 0) AS vs_even_split_pct,
    ROUND(MEDIAN(DATE_DIFF('hour', started, completed) / 24.0), 1)   AS median_assessment_days
FROM a
WHERE completed IS NOT NULL
GROUP BY resource
ORDER BY assessments DESC;
