#!/bin/bash

# Set the path to the DuckDB database file
DB_FILE="superstore_delivered.duckdb"

# Set the path to the directory containing the CSV files
CSV_DIR="../data/csv"

# Array of CSV files to import
CSV_FILES=(
    "crm_customers.csv"
    "delivery_data.csv"
    "ecommerce_products.csv"
    "order_info.csv"
)

# Create the staging schema and import each CSV file
for csv_file in "${CSV_FILES[@]}"; do
    table_name="${csv_file%.csv}"
    
    # Use duckdb to execute SQL commands
    duckdb "$DB_FILE" << EOF
    -- Create staging schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS staging;

    -- Drop the table if it exists
    DROP TABLE IF EXISTS staging.$table_name;

    -- Create and import data into the table
    CREATE TABLE staging.$table_name AS 
    SELECT * FROM read_csv_auto('$CSV_DIR/$csv_file', header=true, filename=true);

    -- Show the first few rows of the imported data
    SELECT * FROM staging.$table_name LIMIT 5;
EOF

    echo "Imported $csv_file into staging.$table_name"
done

echo "All CSV files have been imported into the staging schema in $DB_FILE"