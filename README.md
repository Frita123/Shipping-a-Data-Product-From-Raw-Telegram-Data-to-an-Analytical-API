# Shipping-a-Data-Product-From-Raw-Telegram-Data-to-an-Analytical-API

📦 Shipping a Data Product: Telegram → Analytical API
📌 Project Overview

This project builds an end-to-end data pipeline that:

Collects medical-related Telegram messages

Stores raw data in PostgreSQL

Transforms the data using dbt

Builds an analytical star schema warehouse

Prepares clean data for analytics and APIs

✅ Task 1 — Data Ingestion & Raw Storage
🎯 Objective

Scrape Telegram messages

Clean and normalize the data

Store raw data in PostgreSQL

🛠 What was done

Extracted Telegram messages using Python

Cleaned and structured the data

Created PostgreSQL tables

Loaded data into raw.telegram_messages

📂 Key Outputs

Raw messages stored in PostgreSQL

Reproducible ETL pipeline

Database ready for analytics transformation

✅ Task 2 — Data Warehouse with dbt
🎯 Objective

Transform raw data into an analytical warehouse

Build a star schema using dbt

Add data quality tests and documentation

🛠 What was done

Initialized dbt project (medical_warehouse)

Created models:

stg_telegram_messages (staging)

dim_channels

dim_dates

fct_messages

Implemented:

Not-null tests

Uniqueness tests

Relationship tests

Generated dbt documentation

🏗 Warehouse Schema

Fact Table: fct_messages

Dimensions: dim_channels, dim_dates