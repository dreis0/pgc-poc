from flask import Flask
from routes import roll
from observability import metrics, tracing, logging
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

app = Flask(__name__)

resource = Resource(attributes={
    SERVICE_NAME: "pgc-poc"
})


def configure():
    app.logger.setLevel("DEBUG")

    app.logger.info("Configuring app")

    # register routes
    app.register_blueprint(roll.endpoint)

    metrics.configure_metrics(8000, resource)
    tracing.configure_tracing("http://otel_collector:4317", resource)
    logging.configure_logging(app, "http://otel_collector:4317", resource)


if __name__ == "__main__":
    configure()
    app.run(debug=True, host="0.0.0.0", use_reloader=False)
