import datetime

import sqlalchemy.orm
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
from flask import Flask, request
import time

from sqlalchemy import event, Engine
from sqlalchemy.orm import Session

meter = metrics.get_meter(__name__)

# Demo counter metric
roll_counter = meter.create_counter(
    "roll_counter",
    description="The number of rolls by roll value",
)

request_latency = meter.create_histogram(
    "request_latency",
    description="The latency of requests",
    unit="ms"
)

request_result = meter.create_counter(
    "request_result",
    description="The status code result of requests",
)

database_latency = meter.create_histogram(
    "database_latency",
    description="The latency of database queries",
    unit="ms"
)


def configure_metrics(port, resource):
    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    start_http_server(port, addr="0.0.0.0")


# Metrics middleware class
class MetricsMiddleware:
    app: Flask
    start_time: float
    method: str
    path: str

    def __init__(self, app):
        self.app = app
        self.app.logger.info("Configuring metrics middleware")

        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)

    def before_request(self):
        self.app.logger.info("Starting request")
        self.start_time = time.time()
        self.method = request.method
        self.path = request.path

    def after_request(self, response: Flask.response_class):
        labels = {
            "status_code": response.status_code,
            "method": self.method,
            "path": self.path
        }

        request_latency.record(time.time() - self.start_time, labels)
        request_result.add(1, labels)
        self.app.logger.info("Finishing request")

        return response


class DatabaseMetrics:
    init = None
    finish = None
    type: str = None

    def __init__(self):
        event.listens_for(Engine, "before_cursor_execute")(self.before_query)
        event.listens_for(Engine, "after_cursor_execute")(self.after_query)

    def before_query(self, conn, cursor, statement, parameters, context, executemany):
        self.init = datetime.datetime.utcnow().timestamp()
        self.type = self.get_query_type(statement)

    def after_query(self, conn, cursor, statement, parameters, context, executemany):
        finish = datetime.datetime.utcnow().timestamp()
        database_latency.record((finish - self.init), {"type": self.type})

    def get_query_type(self, statement):
        if statement.startswith("SELECT"):
            return "SELECT"
        elif statement.startswith("INSERT"):
            return "INSERT"
        elif statement.startswith("UPDATE"):
            return "UPDATE"
        elif statement.startswith("DELETE"):
            return "DELETE"
        else:
            return "OTHER"
