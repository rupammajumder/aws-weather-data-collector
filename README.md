# AWS Weather Data Collector 🌦️

## Overview
This project implements a **serverless weather data collection and aggregation pipeline on AWS**.
It periodically fetches weather data from the OpenWeatherMap API, stores it in Amazon S3,
and aggregates recent data into CSV reports.

---

## Architecture
EventBridge → Lambda → S3 → Lambda → CSV Reports → S3  
CloudWatch is used for logging and monitoring.

---

## AWS Services Used
- AWS Lambda (Python)
- Amazon S3
- Amazon EventBridge
- AWS IAM
- Amazon CloudWatch

---

## How It Works
1. EventBridge triggers the weather collector Lambda on a schedule.
2. Lambda fetches weather data for multiple cities.
3. Data is stored in S3 as JSON files.
4. Aggregator Lambda reads recent JSON files from S3.
5. Data is combined and stored as a CSV report in S3.

---

## Security
- API key is stored as an **environment variable**
- IAM roles follow least-privilege principle

---

## Monitoring
- CloudWatch logs capture execution details and errors.

---

## Future Enhancements
- SNS alerts for failures
- Athena for querying historical data
- Terraform for infrastructure provisioning
