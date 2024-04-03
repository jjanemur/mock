FROM python:3.12.1-slim as base

ARG PORT=5000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

COPY . /app

EXPOSE ${PORT}

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
