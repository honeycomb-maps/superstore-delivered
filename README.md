# Superstore Delivered

'Superstore Delivered' contains sample data and transformation logic for an online, delivery-first store.

This repository is meant to be used as a starting point for those implementing data warehouses within logistics, last-mile delivery, and mobility companies. All the data and code is open-source under the MIT License. 

You can find a step-by-step tutorial for building a data warehouse here: 

## Background

If you work in the data industry you may be faimiliar with the ‘Superstore’ dataset from Tableau. The Superstore dataset contained data about the sales performance of a large big-box retailer, including tables like ‘customers’, ‘orders’, ‘products’, etc.

Fast-forward to 2024. Due to lasting changes in consumer behavior driven by the COVID-19 pandemic, Superstore Inc. has seen a dramatic fall in in-store sales. In response to this change in behavior, senior leadership made the decision to switch to a delivery-only business model. 

![Photo by Claudio Schwarz on Unsplash](docs/claudio-schwarz-q8kR_ie6WnI-unsplash.jpg)
_Photo Credit: Claudio Schwarz, Unsplash_

While the migration itself was carried out successfully during the pandemic, the business is now struggling with the unit economics of deliveries. Many delivery failures are occurring, and the cost of labor and equipment for deliveries keeps rising. As the VP of Data, you have been asked to build a series of data products which provide insight into delivery performance.

## Repository Structure
```
.
├── README.md ** this file **
│
├── data
│   ├── csv - ** files in csv format **
│   └── parquet - ** files in parquet format **
│
├── data_generator
│   ├── generate_data.py
│   └── sample_addresses.csv
│
├── dbt - ** code for transforming data with dbt ** 
│
└── docs
    ├── diagrams
    └── images
```

## Downloading the data
You can download pre-generated data files directly from the `data` folder. Data is available in both CSV and Parquet files formats.

## Creating more data
The `data_generator` folder contains a Python script which produces the four data files. You can run it to create your own data:
```sh
python3 data_generator/generate_data.py
```

The file `sample_addresses.csv` contains address and latitude/longitude data from Travis County, Texas. This data is used to ensure realistic delivery points are generated. This data is sourced from the [Texas Geographic Information Office](https://tnris.org/stratmap/address-points.html) and is in the public domain. If you would like to generate sample data for another area, you can substitude this file for your own address data.

You can modify the variables within the `__main__` function in the `generate_data.py` to control the amount of data that is produced. 

## Building the ELT process locally with dbt and DuckDB
1. Install dependencies
    - Python
    - DuckDB
    - dbt (Data Build Tool). _Note: it is suggested to build dbt within it's own virtual python environment with venv_.

2. Initialize the dbt project on your computer
    - `cd dbt`
    - `dbt init`

3. Configure your [dbt profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles) file, using `dbt/profile_template.yml` as a template. You should not need to make any changes to the duckdb settings, but you will need to add your Snowflake credentials if you'd like to run dbt against Snowflake.

4. Run the dbt project locally using DuckDB
```sh
dbt run
```

5. Use the DuckDB CLI (Or a database client like DBeaver) to view the generated tables
```sh
duckdb superstore_delivered.duckdb
SHOW ALL TABLES;
SELECT * FROM metrics_by_h3 LIMIT 10;
```

## 
1. Create virtual env
`python3 -m venv dbt-env`
`source dbt-env/bin/activate`

2. Install dbt
pip3 install dbt-duckdb

3. Project setup
```
dbt init superstore_ecommerce_dw
cd superstore_ecommerce_dw
```

