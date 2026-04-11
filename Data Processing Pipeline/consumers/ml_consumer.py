import json
import os
import time
from collections import deque
import numpy as np
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
WINDOW_SIZE = 20
RSI_PERIOD = 14
MA_PERIOD = 5


def get_kafka_clients():
    while True:
        try:
            consumer = KafkaConsumer(
                "stock-raw",
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_deserializer=lambda m: json.loads(m.decode()),
                auto_offset_reset="latest",
                group_id="ml-consumer-group",
            )
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_serializer=lambda v: json.dumps(v).encode(),
            )
            print("Connected to Kafka", flush=True)
            return consumer, producer
        except NoBrokersAvailable:
            print("Waiting for Kafka broker...", flush=True)
            time.sleep(5)


def compute_rsi(closes, period=RSI_PERIOD):
    if len(closes) < period + 1:
        return None
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100.0 - (100.0 / (1.0 + rs)), 2)


def compute_ma(closes, period=MA_PERIOD):
    if len(closes) < period:
        return None
    return round(float(np.mean(closes[-period:])), 4)


def compute_predicted_close(closes):
    if len(closes) < 3:
        return None
    x = np.arange(len(closes), dtype=float)
    y = np.array(closes, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * len(closes) + intercept
    return round(float(predicted), 4)


def main():
    consumer, producer = get_kafka_clients()
    close_window = deque(maxlen=WINDOW_SIZE)
    print("ML consumer started, listening on stock-raw", flush=True)

    for message in consumer:
        data = message.value
        close_price = float(data["close_price"])
        close_window.append(close_price)

        closes = list(close_window)
        enriched = {
            "timestamp": data["timestamp"],
            "symbol": data["symbol"],
            "open_price": data["open_price"],
            "close_price": close_price,
            "predicted_close": compute_predicted_close(closes),
            "rsi_14": compute_rsi(closes),
            "ma_5": compute_ma(closes),
        }
        producer.send("stock-predictions", enriched)
        producer.flush()
        print(
            f"Published prediction: close={close_price}, "
            f"pred={enriched['predicted_close']}, rsi={enriched['rsi_14']}",
            flush=True,
        )


if __name__ == "__main__":
    main()
