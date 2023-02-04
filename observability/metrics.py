from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

meter = metrics.get_meter(__name__)

# Demo counter metric
roll_counter = meter.create_counter(
        "roll_counter",
        description="The number of rolls by roll value",
    )


def configure_metrics(port, resource):
    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    start_http_server(port, addr="0.0.0.0")
