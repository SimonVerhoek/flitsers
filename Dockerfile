FROM python:3.11-slim

WORKDIR flitserdata

COPY requirements-prod.txt /flitserdata/
COPY requirements-flitsers-dev.txt /flitserdata/

RUN apt-get update \
    && apt-get install -y build-essential bash vim tor \
    && pip3 install --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r requirements-flitsers-dev.txt

COPY . /flitserdata

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
