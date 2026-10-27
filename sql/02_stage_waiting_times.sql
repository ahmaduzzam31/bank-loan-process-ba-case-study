-- Where does the time go? Elapsed time between each activity and the next one in the same case (LEAD).
WITH steps AS (
    SELECT
        case_id,
        activity,
        LEAD(activity)  OVER (PARTITION BY case_id ORDER BY timestamp) AS next_activity,
        DATE_DIFF('hour', timestamp, LEAD(timestamp) OVER (PARTITION BY case_id ORDER BY timestamp)) / 24.0 AS days_to_next
    FROM event_log
)
SELECT
    activity || '  ->  ' || next_activity    AS transition,
    COUNT(*)                                 AS occurrences,
    ROUND(MEDIAN(days_to_next), 1)           AS median_days,
    ROUND(AVG(days_to_next), 1)              AS avg_days,
    ROUND(SUM(days_to_next), 0)              AS total_case_days
FROM steps
WHERE next_activity IS NOT NULL
GROUP BY transition
HAVING COUNT(*) >= 100
ORDER BY total_case_days DESC
LIMIT 12;
