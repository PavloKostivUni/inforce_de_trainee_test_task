# Answers:

## 2. SQL:
### Task 1:
If two deliveries of the same event share the exact same ingested_at only one raw is kept, and because NULL in DESC is sorted after numbers the row with a not null revenue_usd is selected, then. To make result deterministic, I use TO_JSON_STRING(t) to pick a column based on its contents, it's important, because it assures we get the same row chosen on every run of the query.
### Task 2:
Yes, it does matter for the 7-day moving average, because query will use 6 previous rows even if they were more than 7 days before the current event_date. To fix this I would create a table with all dates for every app_id, then left join it with current table and replace NULL with 0.
### Task 3:
I used Inner Join, it doesn't affect columns revenue_usd and cost_usd, because they are not join keys, so when they are NULL the row is still accepted. When revenue_usd is NULL it means that no revenue was produced by the campaign, so ROAS is zero; when cost_usd is NULL, ROAS becomes 0 too, because if we didn't spend money on the campaign or the data about how much we spend is missing we can't and don't need to calculate ROAS. To prevent division by zero error I used SAFE_DIVIDE(ec.revenue_usd, cc.cost_usd) for ROAS calculation.
### Task 4:
I pick up rows based on ingested_at, event_time is recorded first, one time event is created, and then ingested_at, so we receive more recent data if we get the latest ingested_at

## 3. Python:
### Task 2:
If my script dies during df.to_parquet(events_out_path, partition_cols=['event_date']) the events output folder will remain with old partitions deleted and new half way recorded. Because of shutil.rmtree(events_out_path, ignore_errors=True) we lose old data and if new one isn't recorded we end up loosing data. To make it safe, I would first record new parquet files in a temporary folder, than delete old and rename the temp folder. If we crash during these three steps, we can continue them on a new run.
### Task 3:
Columns event_time and ingested_at aren't converted to the datetime format. Function filters by day using string comparison, which is not correct, I changed it to comparing by pulling day from datetime. Converting to float by astype will raise an error when there is a non numeric string, so I changed it to to_numeric with errors='coerce' and added some cleaning. For loop creates a dictionary with app_id and media_source combined to a key and calcuates revenue for them, it is bad for performance because it has to iterate through every row and creating a key like that breaks the principle of atomicity, instead I grouped by these two columns and did a sum of revenue_usd.

## 4. Modelling and design:
### 4.1 Star schema:
Fact table: fact_event. Grain: One row per unique event_id. Measure: revenue_usd. Dimensions: dim_campaign, dim_app, dim_user, dim_date, dim_country, dim_event_name.
### 4.2 A dimension that changes:
Add columns that specify when the campaign was valid, so for the same campaign we will have two rows, but each with a different name and it's validity date. This adds complexity because we have to search the key and then check whether its valid.
### 4.3 Idempotency
Idempotency means running the same job several times but getting the same result as from running it just once. INSERT ... SELECT isn't idempotent because it appends the table every time you run it. As a fix we can try deleting a record and inserting within the same transaction for the same row.
### 4.4 Late data
The event arrives with event_time = Monday and ingested_at = Thursday. The event arrives on Thursday and overwrites row with new data, and because we partition parquet files by event_date the row goes to Monday's partition. I would explain to the client that event arrived late and generated such revenue.
### 4.5 Partitioning
I would partition by event_date because event can arrive multiple times with different ingested_at but always the same event_date, so if we partition by ingested_at copies of one event will be spread across multiple partitions. My choice makes searching by ingested_at slower, because we can't prune a partition we need.
## 5. Debugging scenario
I would check if the data is missing in the table or just on the dashboard. If it's present in the table then problem is with the dashboard.<br>
I would check whether there is raw data for this app. If yes then it was lost during cleaning or loading.
I would check the amount of rows in and out after every cleaning step to decide why exactly was it dropped. 