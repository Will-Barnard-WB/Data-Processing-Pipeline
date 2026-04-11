import json
import os
import time
import psycopg2
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "airflow")
DB_PASS = os.environ.get("DB_PASS", "airflow")


def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )


def get_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                "stock-predictions",
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_deserializer=lambda m: json.loads(m.decode()),
                auto_offset_reset="latest",
                group_id="postgres-consumer-group",
            )
            print("Connected to Kafka", flush=True)
            return consumer
        except NoBrokersAvailable:
            print("Waiting for Kafka broker...", flush=True)
            time.sleep(5)


def main():
    consumer = get_consumer()
    conn = get_db_connection()
    cur = conn.cursor()
    print("Postgres consumer started, listening on stock-predictions", flush=True)

    for message in consumer:
        data = message.value
        try:
            cur.execute(
                """
                INSERT INTO stock_data
                    (dt, stock_symbol, open_price, close_price,
                     predicted_close, rsi_14, ma_5)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (dt, stock_symbol) DO UPDATE SET
                    open_price = EXCLUDED.open_price,
                    close_price = EXCLUDED.close_price,
                    predicted_close = EXCLUDED.predicted_close,
                    rsi_14 = EXCLUDED.rsi_14,
                    ma_5 = EXCLUDED.ma_5
                """,
                (
                    data["timestamp"],
                    data["symbol"],
                    data["open_price"],
                    data["close_price"],
                    data.get("predicted_close"),
                    data.get("rsi_14"),
                    data.get("ma_5"),
                ),
            )
            conn.commit()
            print(f"Inserted {data['symbol']} @ {data['timestamp']}", flush=True)
        except Exception as e:
            print(f"DB error: {e}", flush=True)
            conn.rollback()
            try:
                conn = get_db_connection()
                cur = conn.cursor()
            except Exception:
                pass


if __name__ == "__main__":
    main()
