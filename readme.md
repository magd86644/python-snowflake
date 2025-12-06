## Overview

Use Python's pandas with Snowflake's `write_pandas()` to load CSV data into a Snowflake table directly from a DataFrame.

## Highlights

- Fast and efficient — avoids intermediate file management.  
- Fully Pythonic — operate directly on pandas DataFrames.  
- Only the table is stored in Snowflake; the original CSV file is not uploaded.

## How it works

- Create a DataFrame from your CSV with `pandas.read_csv(...)`.  
- Call `write_pandas(conn, df, table_name)` to write rows into the Snowflake table.  
- No `PUT` command is used, so the CSV file does not get stored in a Snowflake stage.

## Alternatives

- If you need the CSV preserved in Snowflake (e.g., for auditing or reloading), use `PUT` + `COPY INTO` to upload the file to a stage before loading.

## Notes

- Choose `write_pandas()` for simplicity and speed when you don't need the raw CSV in Snowflake.  
- Use staged files (`PUT` + `COPY INTO`) when you require file persistence or staged processing.