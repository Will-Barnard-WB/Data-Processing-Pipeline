# Data-Processing-Pipeline

# 📊 Data Processing Pipeline with Yahoo Finance, PostgreSQL, Docker, and Airflow

## 🚀 Project Overview
This project is a **real-time stock data processing pipeline** that retrieves stock prices from the **Yahoo Finance API**, stores them in a **PostgreSQL database**, and automates the workflow using **Apache Airflow DAGs**. The entire system runs within **Docker containers** for easy deployment and scalability.

## 📌 Features
- Fetches **real-time stock data** from the **Yahoo Finance API**.
- Stores the data in a **PostgreSQL database**.
- Uses **Apache Airflow DAGs** for scheduling, automation, and logging.
- Runs inside **Docker containers** for seamless deployment.
- Logs all key events for monitoring and debugging.

## 🛠️ Tech Stack
- **Yahoo Finance API** (`yfinance` Python library)
- **PostgreSQL** for data storage
- **Apache Airflow** for workflow automation
- **Docker** for containerized deployment
- **Python** for data processing

## 📂 Project Structure
```
├── dags/
    ├── DAG1.py                  # Apache Airflow DAG for stock-data retriveal and storage automation
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── Dockerfile                  # Docker image configuration (defines environment, dependencies, and setup)
```

## Future Improvements
- **Spark:** Advanced data manipulation.
- **Airbyte/Redis** Real-Time data ingestion.



