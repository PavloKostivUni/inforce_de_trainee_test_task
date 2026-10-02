# I've used gemini AI assistant with such prompts:

## 1. The data:
### Prompt 1.1:
Used AI to create three csv files

## 2. SQL:
### Prompt 2.1:
Used AI to help me authenticate to BigQuery from Python and connect to console.cloud.google.com
### Prompt 2.2:
Asked why don`t i see no table nor error (added .result() method, I had an error with not specifying dataset for the table)
### Prompt 2.3
Asked how to make result deterministic -> TO_JSON_STRING(t)
### Prompt 2.4
Asked how to clean revenue_usd and turn it into float -> SAFE_CAST(REPLACE(revenue_usd, ',', '.') AS FLOAT64)
### Prompt 2.5
Asked how to get AVG of current and 6 previous rows
### Prompt 2.6
Asked how to avoid division by zero error
### Prompt 2.7
Asked to help me with incremental load and merge

## 3. Python:
### Prompt 3.1:
Asked to help me with matching strings
### Prompt 3.2 
Asked how to convert to type without crashing on malformed row
### Prompt 3.3 
Asked how to make sort deterministic
### Prompt 3.4
Asked how to parse arguments
### Prompt 3.4
Asked how to delete old parquet files