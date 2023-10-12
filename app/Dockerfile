FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.6.1 \
  PATH=$PATH:/app

WORKDIR app

RUN apt-get update \
    && apt-get install -y build-essential bash vim tor \
    && pip3 install --upgrade pip setuptools

COPY pyproject.toml poetry.lock ./

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

ENV PATH="$PATH:/root/.local/bin"

RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./app/ /app


# Do nothing but keep running
#ENTRYPOINT ["tail", "-f", "/dev/null"]
