# I`ve used BigQuery dialect

from google.cloud import bigquery

client = bigquery.Client(project="lateral-journey-449614-g5")

query = """
    WITH daily as (
        SELECT app_id, DATE(event_time) as event_date, SUM(revenue_usd) as daily_revenue
        FROM `lateral-journey-449614-g5.inforce_test_task_dataset.events_clean`
        GROUP BY app_id, DATE(event_time)
        ORDER BY app_id, event_date
        LIMIT 1000
    )
    SELECT app_id, event_date, daily_revenue,
        SUM(daily_revenue) OVER (
            PARTITION BY app_id
        ) AS total_revenue,
        AVG(daily_revenue) OVER (
            PARTITION BY app_id ORDER BY event_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS moving_avg_7_day,
        SAFE_DIVIDE(
            daily_revenue - LAG(daily_revenue) OVER (
                PARTITION BY app_id ORDER BY event_date
            ),
            LAG(daily_revenue) OVER (
                PARTITION BY app_id ORDER BY event_date
            )
        ) * 100
        as change_in_revenue_pct
    FROM daily 
"""

df = client.query(query).to_dataframe()
print(df)