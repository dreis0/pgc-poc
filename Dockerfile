# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install flask
RUN pip3 install opentelemetry-distro
RUN pip3 install opentelemetry-exporter-otlp
RUN pip3 install opentelemetry-exporter-prometheus
RUN pip3 install prometheus-client


RUN opentelemetry-bootstrap -a install

COPY . .
CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0"]