import os
import time
from flask import Flask
import psycopg2
# Import Prometheus metrics types and the WSGI middleware
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# Define custom Prometheus metrics
REQUEST_COUNT = Counter(
    "flask_app_requests_total", 
    "Total number of HTTP requests", 
    ["method", "endpoint", "status"]
)
DB_LATENCY = Histogram(
    "flask_app_db_connection_seconds", 
    "Time spent connecting to the database"
)

# Plug in Prometheus internal metrics endpoint (/metrics)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

def get_db_connection():
    for _ in range(5):
        try:
            # Measure time spent connecting to DB
            with DB_LATENCY.time():
                conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
            return conn
        except psycopg2.OperationalError:
            time.sleep(2)
    return None

@app.route("/")
def hello():
    status_code = 200
    conn = get_db_connection()
    
    if conn:
        conn.close()
        db_status = "Connected to Database Successfully!"
    else:
        db_status = "Database Connection Failed."
        status_code = 500

    # Increment the counter with specific dimension labels
    REQUEST_COUNT.labels(method="GET", endpoint="/", status=status_code).inc()
    
    return f"Hello, World! Status: {db_status}", status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
