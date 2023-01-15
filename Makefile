
run-collector:
	docker run -p 4317:4317 \
		-v ~/Documents/Repos/ufabc/pgc-getting-started/tmp/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
		otel/opentelemetry-collector:latest \
		--config=/etc/otel-collector-config.yaml

run-app:
	@flask --app app --debug run