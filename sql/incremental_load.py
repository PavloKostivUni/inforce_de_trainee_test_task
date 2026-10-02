# I`ve used BigQuery dialect

from google.cloud import bigquery

client = bigquery.Client(project="lateral-journey-449614-g5")

staging_table_query = """
    CREATE TABLE IF NOT EXISTS inforce_test_task_dataset.events_staging AS
    SELECT * EXCEPT (rn, revenue_usd), SAFE_CAST(REPLACE(revenue_usd, ',', '.') AS FLOAT64) AS revenue_usd
    FROM (
        SELECT t.*, ROW_NUMBER() OVER 
            (PARTITION BY event_id ORDER BY 
                ingested_at DESC, 
                SAFE_CAST(REPLACE(revenue_usd, ',', '.') AS FLOAT64) DESC,
                TO_JSON_STRING(t) DESC
            ) as rn
        FROM `lateral-journey-449614-g5.inforce_test_task_dataset.events_raw` as t
        WHERE is_test IS NOT TRUE
    )
    WHERE rn = 1
    LIMIT 100
"""

client.query(staging_table_query).result()

test_query = """
    MERGE INTO `inforce_test_task_dataset.events_clean` AS clean
    USING `inforce_test_task_dataset.events_staging` as source
    ON (clean.event_id = source.event_id)
    WHEN MATCHED AND source.ingested_at > clean.ingested_at THEN
        UPDATE SET
            user_id = source.user_id,
            app_id = source.app_id,
            event_name = source.event_name,
            event_time = source.event_time,
            ingested_at = source.ingested_at,
            country = source.country,
            media_source = source.media_source,
            campaign = source.campaign,
            revenue_usd = source.revenue_usd,
            is_test = source.is_test
    WHEN NOT MATCHED THEN
        INSERT ROW
"""

df = client.query(test_query).to_dataframe()
print(df)