import os
import time
import psycopg2
import pandas as pd
import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Real-Time Anomaly Dashboard",
    layout="wide"
)

st.title("🚨 Real-Time Anomaly Detection Dashboard")

REFRESH_INTERVAL = 5  # seconds

# -----------------------------
# Database Config
# -----------------------------
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "anomalies_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "anomaly_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "anomaly_pass")

# -----------------------------
# Database Fetch Function
# -----------------------------
def fetch_anomalies():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    query = """
        SELECT
            device_id,
            event_timestamp,
            metric_value,
            mean_value,
            std_dev_value,
            processed_at
        FROM anomalies
        ORDER BY processed_at DESC
        LIMIT 100;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -----------------------------
# Auto Refresh
# -----------------------------
placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("Latest Detected Anomalies")

        try:
            df = fetch_anomalies()

            if df.empty:
                st.info("No anomalies detected yet.")
            else:
                st.dataframe(df, use_container_width=True)

                st.subheader("Metric Trend (Latest 50)")
                st.line_chart(
                    df.head(50).set_index("processed_at")["metric_value"]
                )

        except Exception as e:
            st.error(f"Database connection error: {e}")

    time.sleep(REFRESH_INTERVAL)
