import json
import os
import time
import random
from datetime import datetime
from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("RAW_TOPIC", "raw_events")
EVENT_RATE = int(os.getenv("EVENT_RATE", 1))  # events per second

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

device_ids = [f"device_{i}" for i in range(1, 6)]

print("🚀 Producer started...")

while True:
    event = {
        "device_id": random.choice(device_ids),
        "timestamp": datetime.utcnow().isoformat(),
        "metric": round(random.uniform(40, 120), 2)
    }

    producer.send(TOPIC, event)
    print("📤 Sent event:", event)

    time.sleep(1 / EVENT_RATE)
