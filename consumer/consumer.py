import json
import os
import time
from collections import deque, defaultdict
from statistics import mean, stdev

from kafka import KafkaConsumer, KafkaProducer
import psycopg2
from psycopg2.extras import execute_values


# -----------------------------
# Environment Variables
# -----------------------------
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
RAW_TOPIC = os.getenv("RAW_TOPIC", "raw_events")
ANOMALY_TOPIC = os.getenv("ANOMALY_TOPIC", "anomalies")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "anomalies_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "anomaly_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "anomaly_pass")

WINDOW_SIZE = 20
STD_THRESHOLD = 2


# -----------------------------
# PostgreSQL Connection
# -----------------------------
def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )


# -----------------------------
# Kafka Consumer & Producer
# -----------------------------
consumer = KafkaConsumer(
    RAW_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="anomaly-detector-group"
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


# -----------------------------
# Stateful Windows
# -----------------------------
windows = defaultdict(lambda: deque(maxlen=WINDOW_SIZE))


# -----------------------------
# Main Loop
# -----------------------------
def main():
    print("🚀 Anomaly Consumer started. Waiting for events...")

    db_conn = get_db_connection()
    db_cursor = db_conn.cursor()

    try:
        for message in consumer:
            event = message.value
            device_id = event["device_id"]
            metric = event["metric"]
            timestamp = event["timestamp"]

            window = windows[device_id]
            window.append(metric)

            # Need enough data to compute std deviation
            if len(window) < 10:
                continue

            avg = mean(window)
            deviation = stdev(window)

            if deviation == 0:
                continue

            # Anomaly check
            if abs(metric - avg) > STD_THRESHOLD * deviation:
                anomaly = {
                    "device_id": device_id,
                    "event_timestamp": timestamp,
                    "metric_value": metric,
                    "mean_value": round(avg, 2),
                    "std_dev_value": round(deviation, 2)
                }

                print(f"🚨 ANOMALY DETECTED: {anomaly}")

                # Publish to Kafka anomalies topic
                producer.send(ANOMALY_TOPIC, anomaly)

                # Insert into PostgreSQL
                insert_sql = """
                    INSERT INTO anomalies
                    (device_id, event_timestamp, metric_value, mean_value, std_dev_value)
                    VALUES (%s, %s, %s, %s, %s)
                """

                db_cursor.execute(
                    insert_sql,
                    (
                        anomaly["device_id"],
                        anomaly["event_timestamp"],
                        anomaly["metric_value"],
                        anomaly["mean_value"],
                        anomaly["std_dev_value"]
                    )
                )

                db_conn.commit()

    except Exception as e:
        print("❌ Error in consumer:", e)

    finally:
        db_cursor.close()
        db_conn.close()
        consumer.close()
        producer.close()


if __name__ == "__main__":
    main()
