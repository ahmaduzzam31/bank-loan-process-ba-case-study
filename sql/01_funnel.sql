-- Application funnel: how many applications reach each milestone, and where are they lost?
WITH milestones AS (
    SELECT * FROM (VALUES
        (1, 'Application submitted'), (2, 'KYC/AML checks completed'), (3, 'Credit assessment completed'),
        (4, 'Loan offer issued'), (5, 'Offer accepted'), (6, 'Loan funded')) AS m(step, activity)
)
SELECT
    m.step,
    m.activity                                                          AS milestone,
    COUNT(DISTINCT e.case_id)                                           AS applications,
    ROUND(100.0 * COUNT(DISTINCT e.case_id) / FIRST_VALUE(COUNT(DISTINCT e.case_id)) OVER (ORDER BY m.step), 1) AS pct_of_submitted
FROM milestones m
LEFT JOIN event_log e ON e.activity = m.activity
GROUP BY m.step, m.activity
ORDER BY m.step;
