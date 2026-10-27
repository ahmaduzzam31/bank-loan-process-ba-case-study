-- Customers walk away when we are slow. For APPROVED applications, how often does the customer still
-- withdraw (or reject the offer), by how long the credit decision took?
WITH c AS (
    SELECT
        e.case_id,
        a.outcome,
        DATE_DIFF('hour',
            MIN(e.timestamp) FILTER (WHERE e.activity = 'Application submitted'),
            MIN(e.timestamp) FILTER (WHERE e.activity IN ('Credit committee decision', 'Delegated authority decision'))
        ) / 24.0 AS days_to_decision
    FROM event_log e JOIN applications a USING (case_id)
    GROUP BY e.case_id, a.outcome
)
SELECT
    CASE WHEN days_to_decision < 10 THEN '1: < 10 days' WHEN days_to_decision < 15 THEN '2: 10-14 days'
         WHEN days_to_decision < 20 THEN '3: 15-19 days' WHEN days_to_decision < 25 THEN '4: 20-24 days'
         ELSE '5: 25+ days' END                                              AS time_to_decision,
    COUNT(*)                                                                 AS approved_applications,
    ROUND(100.0 * AVG(CASE WHEN outcome = 'Withdrawn' THEN 1 ELSE 0 END), 1) AS lost_after_approval_pct
FROM c
WHERE days_to_decision IS NOT NULL AND outcome <> 'Declined'
GROUP BY 1
ORDER BY 1;
