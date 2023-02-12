from flask import Flask
from database.configure import configure_database
from middleware.auth import AuthMiddleware
from observability import metrics, tracing, logging
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from flask_sqlalchemy import SQLAlchemy

from routes.auth import AuthEndpoint
from routes.roll import RollDiceEndpoint

app = Flask(__name__)

resource = Resource(attributes={
    SERVICE_NAME: "pgc-poc"
})


def configure():
    app.logger.setLevel("DEBUG")

    app.logger.info("Configuring app")

    database_url = "postgresql://postgres:postgres@postgres:5432/dice"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    db = SQLAlchemy(app)
    configure_database(app, db)

    # add observability middlewares
    FlaskInstrumentor().instrument_app(app)
    with app.app_context():
        SQLAlchemyInstrumentor().instrument(engine=db.engine, enable_commenter=True)

    metrics.configure_metrics(8000, resource)
    metrics.MetricsMiddleware(app)
    metrics.DatabaseMetrics()

    tracing.configure_tracing("http://otel_collector:4317", resource)

    logging.configure_logging(app, "http://otel_collector:4317", resource)

    # add custom middlewares
    AuthMiddleware(app, "super-secret")

    # register routes
    app.register_blueprint(RollDiceEndpoint(app).blueprint)
    app.register_blueprint(AuthEndpoint(app, db, "super-secret").blueprint)


if __name__ == "__main__":
    configure()
    app.run(debug=True, port=5001, host="0.0.0.0", use_reloader=False)
