import json
import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "airflow")
DB_PASS = os.environ.get("DB_PASS", "airflow")
KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


def get_db_connection():
    try:
        return psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
        )
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def kafka_listener():
    import time
    from kafka import KafkaConsumer
    from kafka.errors import NoBrokersAvailable

    while True:
        try:
            consumer = KafkaConsumer(
                "stock-predictions",
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_deserializer=lambda m: json.loads(m.decode()),
                auto_offset_reset="latest",
                group_id="flask-socketio-group",
            )
            print("Flask Kafka listener connected", flush=True)
            for message in consumer:
                data = message.value
                payload = {
                    "datetime": data.get("timestamp"),
                    "symbol": data.get("symbol"),
                    "open_price": data.get("open_price"),
                    "close_price": data.get("close_price"),
                    "predicted_close": data.get("predicted_close"),
                    "rsi_14": data.get("rsi_14"),
                    "ma_5": data.get("ma_5"),
                }
                socketio.emit("stock_update", payload)
        except NoBrokersAvailable:
            print("Kafka not available, retrying in 5s...", flush=True)
            time.sleep(5)
        except Exception as e:
            print(f"Kafka listener error: {e}", flush=True)
            time.sleep(5)


@app.route("/", methods=["GET"])
def get_stock_data():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT dt, stock_symbol, open_price, close_price,
                   predicted_close, rsi_14, ma_5
            FROM stock_data
            ORDER BY dt DESC
            LIMIT 50
            """
        )
        rows = cur.fetchall()
        stocks = [
            {
                "datetime": row[0],
                "symbol": row[1],
                "open_price": row[2],
                "close_price": row[3],
                "predicted_close": row[4],
                "rsi_14": row[5],
                "ma_5": row[6],
            }
            for row in rows
        ]
        return jsonify({"stocks": list(reversed(stocks))})
    except Exception as e:
        return jsonify({"error": f"Error fetching stock data: {str(e)}"}), 500
    finally:
        cur.close()
        conn.close()


socketio.start_background_task(kafka_listener)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5050)
