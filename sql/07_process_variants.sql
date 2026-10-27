-- Process variants: the most common end-to-end paths (process mining "variant analysis").
WITH paths AS (
    SELECT case_id, STRING_AGG(activity, ' > ' ORDER BY timestamp) AS path
    FROM event_log GROUP BY case_id
)
SELECT
    ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC)          AS variant,
    COUNT(*)                                            AS applications,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)  AS pct,
    path
FROM paths
GROUP BY path
ORDER BY applications DESC
LIMIT 8;
