-- Approval route: wait from "credit assessment completed" to decision, committee vs delegated authority.
WITH x AS (
    SELECT
        case_id,
        MIN(timestamp) FILTER (WHERE activity = 'Credit assessment completed') AS assessed,
        MIN(timestamp) FILTER (WHERE activity = 'Credit committee decision')   AS committee,
        MIN(timestamp) FILTER (WHERE activity = 'Delegated authority decision') AS delegated
    FROM event_log GROUP BY case_id
)
SELECT
    CASE WHEN committee IS NOT NULL THEN 'Credit committee (>= €100k)' ELSE 'Delegated authority (< €100k)' END AS route,
    COUNT(*)                                                                         AS decisions,
    ROUND(MEDIAN(DATE_DIFF('hour', assessed, COALESCE(committee, delegated)) / 24.0), 1) AS median_wait_days,
    ROUND(QUANTILE_CONT(DATE_DIFF('hour', assessed, COALESCE(committee, delegated)) / 24.0, 0.9), 1) AS p90_wait_days
FROM x
WHERE COALESCE(committee, delegated) IS NOT NULL
GROUP BY route;
