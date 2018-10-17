FROM python:3.7-stretch

WORKDIR flitsers

COPY requirements-flitsers.txt /flitsers/

RUN apt-get update \
    && apt-get install -y build-essential bash vim \
    && pip3 install --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r requirements-flitsers.txt \
    && rm -r /root/.cache

COPY . /flitsers

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
