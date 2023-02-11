# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r ./requirements.txt
RUN opentelemetry-bootstrap -a install

EXPOSE 5001

CMD ["python3", "api.py"]
# CMD ["opentelemetry-instrument", "flask", "run"]