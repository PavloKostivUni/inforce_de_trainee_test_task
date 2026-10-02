# I`ve used BigQuery dialect

from google.cloud import bigquery

client = bigquery.Client(project="lateral-journey-449614-g5")

query = """
    SELECT ec.app_id, TRIM(ec.media_source) AS media_source, TRIM(ec.campaign) as campaign, 
        ec.event_date, ec.revenue_usd, cc.cost_usd, 
        COALESCE(SAFE_DIVIDE(ec.revenue_usd, cc.cost_usd), 0) as ROAS
    FROM (
        SELECT app_id, media_source, campaign, SUM(revenue_usd) as revenue_usd, DATE(event_time) as event_date
        FROM `inforce_test_task_dataset.events_clean`
        GROUP BY app_id, media_source, campaign, DATE(event_time)
    ) as ec
    JOIN `inforce_test_task_dataset.campaign_costs` as cc
    ON ec.app_id = cc.app_id 
        AND LOWER(TRIM(ec.media_source)) = LOWER(TRIM(cc.media_source)) 
        AND LOWER(TRIM(ec.campaign)) = LOWER(TRIM(cc.campaign))
        AND ec.event_date = DATE(cc.date)
"""

df = client.query(query).to_dataframe()
print(df)