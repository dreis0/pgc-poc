from flask import Flask
from routes import roll
from observability import metrics
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

    app.logger.info("Starting Prometheus exporter")
    metrics.configure_metrics(8000, resource)


if __name__ == "__main__":
    configure()
    app.run(debug=True,host="0.0.0.0", use_reloader=False)
