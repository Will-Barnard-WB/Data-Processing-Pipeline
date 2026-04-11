from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
import yfinance as yf


def get_stock_data(**kwargs):
    stock = yf.Ticker("AAPL")
    data = stock.history(period="1d", interval="1m", prepost=True)
    latest_data = data.iloc[-1]
    current_open = latest_data["Open"]
    current_close = latest_data["Close"]
    kwargs["ti"].xcom_push(key="current_open", value=current_open)
    kwargs["ti"].xcom_push(key="current_close", value=current_close)


def produce_to_kafka(**kwargs):
    from kafka import KafkaProducer
    import json
    import os
    ti = kwargs["ti"]
    producer = KafkaProducer(
        bootstrap_servers=os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        value_serializer=lambda v: json.dumps(v).encode(),
    )
    producer.send("stock-raw", {
        "timestamp": kwargs["ts"],
        "symbol": "AAPL",
        "open_price": ti.xcom_pull(task_ids="fetch_stock_data", key="current_open"),
        "close_price": ti.xcom_pull(task_ids="fetch_stock_data", key="current_close"),
    })
    producer.flush()


default_args = {
    "owner": "admin",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_yfinance",
    default_args=default_args,
    start_date=datetime(2025, 2, 26, 10, 33, 0),
    schedule_interval="* * * * *",
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_stock_data",
        python_callable=get_stock_data,
        provide_context=True,
    )

    task1 = SQLExecuteQueryOperator(
        task_id="create_postgres_table",
        conn_id="postgres_localhost",
        sql=(
            "CREATE TABLE IF NOT EXISTS stock_data ("
            "dt TIMESTAMP, "
            "stock_symbol VARCHAR, "
            "open_price DOUBLE PRECISION, "
            "close_price DOUBLE PRECISION, "
            "predicted_close DOUBLE PRECISION, "
            "rsi_14 DOUBLE PRECISION, "
            "ma_5 DOUBLE PRECISION, "
            "PRIMARY KEY (dt, stock_symbol)"
            ");"
        ),
    )

    produce_task = PythonOperator(
        task_id="produce_to_kafka",
        python_callable=produce_to_kafka,
        provide_context=True,
    )

    task4 = SQLExecuteQueryOperator(
        task_id="delete_oldest_stock_data",
        conn_id="postgres_localhost",
        sql=(
            "DELETE FROM stock_data "
            "WHERE dt IN ("
            "SELECT dt FROM stock_data "
            "WHERE stock_symbol = 'AAPL' "
            "ORDER BY dt DESC OFFSET 10"
            ");"
        ),
    )

    fetch_task >> task1 >> produce_task >> task4
