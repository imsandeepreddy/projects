import os
import logging
from flask import Flask

app = Flask(__name__)

# Configure Flask logging format
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

@app.route("/")
def home():
    db_url = os.getenv("DATABASE_URL")
    
    # Trigger error if config is missing
    if not db_url:
        app.logger.error("Configuration Error: 'DATABASE_URL' environment variable is missing!")
        return "Internal Server Error: Missing Config", 500
        
    # Trigger error if config is wrong
    if "prod-db" not in db_url:
        app.logger.warning("Database configuration mismatch. Detected fallback URL: %s", db_url)
        app.logger.error("Database connection failed!\n"
                         "ConnectionRefusedError: [Errno 111] Connection refused\n"
                         "  File \"app.py\", line 18, in home\n"
                         "    db.connect(db_url)")
        return "Internal Server Error: Connection Refused", 500

    app.logger.info("Successfully connected to database at %s", db_url)
    return "Hello, World! Application is healthy."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
