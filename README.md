# Data-Processing-Pipeline

# 📊 Data Processing Pipeline with Yahoo Finance, PostgreSQL, Docker, and Airflow

## 🚀 Project Overview
This project is a **real-time stock data processing pipeline** that retrieves stock prices from the **Yahoo Finance API**, stores them in a **PostgreSQL database**, and automates the workflow using **Apache Airflow DAGs**. The entire system runs within **Docker containers** for easy deployment and scalability.

## 📌 Features
- Fetches **real stock data** from the **Yahoo Finance API**.
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
│   ├── stock_data_pipeline.py   # Apache Airflow DAG for automation
├── db/
│   ├── init.sql                 # PostgreSQL database initialization script
├── services/
│   ├── fetch_stock_data.py      # Script to fetch stock data from Yahoo Finance
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
```

## 🔧 Setup & Installation

### 1️⃣ Clone the repository
```sh
git clone https://github.com/your-username/stock-data-pipeline.git
cd stock-data-pipeline
```

### 2️⃣ Set up environment variables
Create a `.env` file with your database credentials:
```sh
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=stock_data
```

### 3️⃣ Start the services using Docker
```sh
docker-compose up --build
```
This will:
- Start the **PostgreSQL database**.
- Initialize the **Airflow scheduler & webserver**.
- Run the **stock data fetching script**.

### 4️⃣ Access Airflow UI
Once running, go to [http://localhost:8080](http://localhost:8080) and log in:
- **Username:** `airflow`
- **Password:** `airflow`

### 5️⃣ Trigger the DAG manually (Optional)
You can trigger the pipeline manually by enabling the DAG in the Airflow UI or running:
```sh
airflow dags trigger stock_data_pipeline
```

## 📜 Airflow DAG Overview
The **stock_data_pipeline DAG** performs the following:
1. Deletes old stock entries (keeps only the latest 10 records).
2. Fetches new stock data from the Yahoo Finance API.
3. Stores the retrieved data in the PostgreSQL database.
4. Logs execution details.

## 🔍 Logs & Monitoring
- **Airflow logs:** Can be accessed via the Airflow UI.
- **Container logs:** Use `docker logs <container_id>` to inspect individual service logs.
- **PostgreSQL logs:** Stored inside the database container.


