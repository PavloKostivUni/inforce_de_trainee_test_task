# Assumptions:

## 2. SQL:
### Task 1:
I wasn't sure whether I need to put revenue_usd in a clean float format in this task because I saw this requirement in a Task 3.1, but after reading Task 2.2 I decided to clean the revenue_usd in this task.
### Task 3:
There were a lot of organic records in media_source, I decided not to add them to the final table, because they don't bring ROAS information as they don't have a campaign and no money is spent on them.
### Task 4:
I can't do inserts or updates without billing, so I can't do merge into. Also incremental load is something I haven't done before so I just wrote a simple MERGE how AI guided me

## 3. Python:
### Task 3:
Task didn't specify whether colleague wanted to exclude test rows and remove duplicates and just didn't do it, so I did it