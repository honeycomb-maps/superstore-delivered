## Running the ELT process locally with dbt and DuckDB
1. Install dependencies
    - [Python](https://www.python.org/downloads/)
    - [DuckDB](https://duckdb.org/)
    - [dbt (Data Build Tool)](https://docs.getdbt.com/docs/core/installation-overview). _Note: it is suggested to build dbt within it's own virtual python environment with venv_.

2. Initialize the dbt project on your computer
    - `cd dbt`
    - `dbt init`

3. Configure your [dbt profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles) file, using `dbt/profile_template.yml` as a template. You should not need to make any changes to the duckdb settings, but you will need to add your Snowflake credentials if you'd like to run dbt against Snowflake.

4. Run the dbt project locally using DuckDB
```sh
dbt run
```
_Note: the generated data has already been loaded into staging tables in the superstore_delivered.duckdb file for you. This means you can run the transformation logic directly. If you would like to load other data files into the database, you can use the `load_csv_data.sh` script._

You should see some output from dbt, ending with `Completed successfully. Done. PASS=11 WARN=0 ERROR=0 SKIP=0 TOTAL=11`.

**Congrats, you've just successfully built and ran a complete data warehouse on your computer!** 

5. Use the DuckDB CLI (Or a database client like DBeaver) to view the generated tables
```sh
duckdb superstore_delivered.duckdb
SHOW ALL TABLES;
SELECT * FROM metrics_by_h3 LIMIT 10;
```

6. (optional) Export the generated analytics tables to Parquet or CSV for visualization 
```sh
duckdb superstore_delivered.duckdb
SHOW ALL TABLES;
COPY metrics_by_h3 TO 'metrics_by_h3.parquet' (FORMAT PARQUET, COMPRESSION ZSTD); # compression can reduce file size significantly
COPY order_locations_delivery_success TO 'order_locations_delivery_success.csv' (HEADER, DELIMITER ',');
```
