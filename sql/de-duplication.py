# I`ve used BigQuery dialect

from google.cloud import bigquery

client = bigquery.Client(project="lateral-journey-449614-g5")

query = """
    CREATE OR REPLACE TABLE inforce_test_task_dataset.events_clean AS
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
"""

client.query(query).result()

test_query = """
    SELECT COUNT(event_id), COUNT(DISTINCT event_id)
    FROM inforce_test_task_dataset.events_clean
"""

df = client.query(test_query).to_dataframe()
print(df)