## Flask Application Monitoring with Prometheus and Grafana
This repository contains a containerised Python Flask application backed by a PostgreSQL database. The infrastructure includes a complete monitoring stack using Prometheus to scrape metrics and Grafana for visual dashboards.

## Architecture Component Overview

* Flask App (:5000): Python web application instrumented with the Prometheus client library.
* PostgreSQL (:5432): Relational database storage layer.
* Nginx Proxy (:80): Reverse proxy routing external web traffic to the Flask app.
* Node Exporter (:9100): Scrapes container-level infrastructure and hardware metrics.
* Prometheus (:9090): Time-series database engine that pulls metrics from the App and Node Exporter.
* Grafana (:3000): Visualization platform pre-provisioned with the Prometheus data source.

------------------------------
## File Structure

├── app.py                  # Instrumented Flask application
├── docker-compose.yaml     # Full multi-container stack deployment layout
├── nginx.conf              # Reverse proxy routing configurations
├── prometheus.yaml         # Scraping targets configuration mapping
├── grafana-datasource.yml  # Automated Grafana data source configuration
└── requirements.txt        # Python dependencies (Flask, psycopg2-binary, prometheus-client)

------------------------------
## Quick Start Setup

## 1. Spin Up the Stack
Launch all components in the background using Docker Compose:

docker compose up -d

## 2. Generate Traffic
Seed data into your Prometheus metrics by generating a few HTTP requests to the application:
```bash
curl http://localhost/
```

(Run this command 5 to 10 times to populate the charts).
------------------------------
## Metric Verification & Hands-on PromQL
Open the Prometheus UI at http://localhost:9090 and execute these queries in the Graph tab to verify data streams:
## Application Metrics

* Total Request Count:
```
flask_app_requests_total
```
* Request Rate (1-minute window):
```
rate(flask_app_requests_total[1m])
```
* Average DB Connection Latency:
```
sum(flask_app_db_connection_seconds_sum) / sum(flask_app_db_connection_seconds_count)
```

## Infrastructure Metrics

* Container CPU Usage Percentage:
```
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
```
* Available System Memory (MB):
```
node_memory_MemFree_bytes / 1024 / 1024
```

------------------------------
## Grafana Dashboard Access

   1. Navigate to the Grafana interface at http://localhost:3000.
   2. Log in using the default credentials:
        * Username: admin
        * Password: admin
   3. Navigate to Connections > Data Sources to see the automatically pre-loaded Prometheus engine.
   4. Click Create Dashboard > Add a new panel and paste any PromQL query from the section above to build your visualization layout.


