from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)

def configure_logging(app, otel_collector_endpoint, resource):
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter(endpoint=otel_collector_endpoint, insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level="DEBUG", logger_provider=logger_provider)

    # Attach OTLP handler to root logger
    app.logger.addHandler(handler)
