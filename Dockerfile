FROM python:3.12.1-slim as base

ARG PORT=5000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN useradd -m -d /home/python -s /bin/bash python

RUN chown -R python:python /app

ENV HOME=/home/python

ENV PATH="/home/python/.local/bin:${PATH}"

USER python

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

COPY . /app

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
