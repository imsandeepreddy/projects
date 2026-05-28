import os
import time
from flask import Flask
import psycopg2  # Add 'psycopg2-binary' to your requirements.txt

app = Flask(__name__)


def get_db_connection():
    # Retry logic to wait for Postgres to boot up completely
    for _ in range(5):
        try:
            conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
            return conn
        except psycopg2.OperationalError:
            time.sleep(2)
    return None


@app.route("/")
def hello():
    conn = get_db_connection()
    if conn:
        conn.close()
        db_status = "Connected to Database Successfully!"
    else:
        db_status = "Database Connection Failed."

    return f"Hello, World! Status: {db_status}"


if __name__ == "__main__":
    # Internal container port; Nginx maps this to the outside world
    app.run(host="0.0.0.0", port=5000)
