from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from app.routes import app

app.run(host='0.0.0.0', port=8080)
