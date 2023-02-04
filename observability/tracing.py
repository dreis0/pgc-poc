from opentelemetry import trace

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

tracer = trace.get_tracer(__name__)


def configure_tracing(trace_collector_endpoint, resource):
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=trace_collector_endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
