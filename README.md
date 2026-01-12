# 🚨📊 Real-Time Anomaly Detection Pipeline
=====================================================

📌 PROJECT OVERVIEW
------------------
This project implements a complete, production-style
**REAL-TIME DATA STREAMING PIPELINE** to detect anomalies
in continuously generated event data.

The system simulates live device metrics 📡, processes them
using **Apache Kafka**, performs stateful anomaly detection,
stores detected anomalies in **PostgreSQL**, and visualizes
them using a **real-time dashboard** 📈.

This project reflects real-world use cases such as:
- 💳 Fraud detection
- 🌐 IoT device monitoring
- ⚙️ Operational intelligence
- 📊 Streaming analytics systems


🧠 KEY CONCEPTS COVERED
----------------------
- 🔄 Event-driven architecture
- ⏱️ Real-time data streaming
- 📨 Apache Kafka producers and consumers
- 🧮 Stateful stream processing
- 📐 Rolling window statistics
- 🐳 Dockerized microservices
- 📊 Real-time dashboards
- 🛡️ Fault-tolerant data pipelines


🏗️ ARCHITECTURE
---------------
```

Python Producer 🐍
   ↓
Kafka Topic (raw_events) 📨
   ↓
Kafka Consumer (Anomaly Detection) 🚨
   ↓
Kafka Topic (anomalies) 📌
   ↓
PostgreSQL (anomalies table) 🗄️
   ↓
Streamlit Dashboard (Real-Time View) 📈
```

🧩 SYSTEM COMPONENTS
-------------------
1️⃣ Producer
   - Generates continuous synthetic events
   - Publishes events to Kafka topic: raw_events

2️⃣ Kafka
   - Acts as the central message broker
   - Decouples producers and consumers
   - Ensures durability and scalability

3️⃣ Consumer (Anomaly Detector)
   - Consumes events from raw_events
   - Maintains rolling windows per device
   - Detects anomalies using statistical rules
   - Publishes anomalies to anomalies topic

4️⃣ PostgreSQL
   - Persists detected anomalies
   - Acts as the system of record

5️⃣ Dashboard
   - Reads data from PostgreSQL
   - Displays anomalies in near real-time
   - Auto-refreshes every few seconds ⏳


🚨 ANOMALY DETECTION LOGIC
-------------------------
Each device is analyzed **INDEPENDENTLY** using a rolling
statistical window 📊.

Processing steps:
1. 📥 Read incoming event
2. 🆔 Group events by device_id
3. 🪟 Maintain rolling window of last N metrics
4. 📐 Compute mean and standard deviation
5. ⚠️ Apply anomaly detection rule
6. 🚨 Publish anomaly if detected
7. 💾 Persist anomaly to PostgreSQL


📐 DETECTION RULE
----------------
An event is classified as an anomaly if:

|metric_value − mean| > threshold × standard_deviation

Where:
- metric_value : current incoming metric
- mean         : mean of rolling window
- std_dev      : standard deviation of rolling window
- threshold    : configurable (default = 3)
- window size  : configurable (default = 100)

📍 Detection is performed **PER DEVICE**.


⚙️ TECH STACK
-------------
- 📨 Apache Kafka
- 🧭 Zookeeper
- 🐍 Python
- 🗄️ PostgreSQL
- 📊 Streamlit
- 🐳 Docker
- 📦 Docker Compose


🗂️ PROJECT STRUCTURE
--------------------
```

real-time-anomaly-detection-pipeline/
│
├── docker-compose.yml
│
├── producer/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── consumer/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── dashboard/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── postgres/
│   └── init.sql
│
└── README.md
```
---

🚀 SETUP & EXECUTION
-------------------
Prerequisites:
- 🐳 Docker Desktop
- 📦 Docker Compose
- 🌱 Git
- 🐍 Python 3.9+

Steps:
1. Clone the repository
2. Navigate to project directory
3. Run: docker-compose up --build
4. Wait for all services to start ⏳

---

📊 VIEWING OUTPUTS
-----------------
Dashboard 📈:
- URL: http://localhost:8501
- Displays detected anomalies
- Auto-refreshes every few seconds

Consumer Logs 🖥️:
- docker logs -f consumer
- Shows anomaly detection messages in real time

PostgreSQL Validation 🗄️:
- docker exec -it postgres psql -U anomaly_user -d anomalies_db
- Query anomalies table to verify persistence

---

🔐 BEST PRACTICES IMPLEMENTED
-----------------------------
- 🔧 Environment variables for configuration
- ❌ No hardcoded credentials
- 🔗 Decoupled services
- ♻️ Stateless producers and consumers
- 🛑 Graceful shutdown handling
- 🛡️ Fault-tolerant message processing

---

✅ VERIFIED OUTCOMES
------------------
✔ Continuous event streaming  
✔ Real-time anomaly detection  
✔ Kafka topic decoupling  
✔ PostgreSQL persistence  
✔ Live dashboard visualization  
✔ Stable long-running execution  

---

📚 KEY LEARNINGS
---------------
- Designing streaming architectures
- Working with Kafka producers & consumers
- Implementing stateful logic in streaming systems
- Container orchestration using Docker Compose
- Debugging distributed systems
- End-to-end observability of data pipelines

---

🚀 FUTURE ENHANCEMENTS
---------------------
- 🤖 Machine learning-based anomaly detection
- 📩 Alerting via Email / Slack
- 📈 Kafka topic partition scaling
- 📊 Monitoring (Prometheus + Grafana)
- 🔐 Authentication & security
- ☁️ Cloud deployment (AWS / GCP / Azure)

---

🏁 FINAL CONCLUSION
------------------
This project represents a complete, real-world,
production-style **REAL-TIME ANOMALY DETECTION PIPELINE** 🚨.

It is suitable for:
- 📁 Data engineering portfolios
- 💼 Technical interviews
- 🎓 Hands-on learning
- 🧠 Demonstrating streaming system expertise

