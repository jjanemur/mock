# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.1
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


# Create a non-privileged user that the app will run under.
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     appuser
#
# RUN mkdir /app
# RUN chown -R appuser:appuser /app

# Switch to the non-priviledged user
# USER appuser

# Set the working directory
WORKDIR /app

# Copy the Pipfile an Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install dependencies from Pipfile.lock
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

# Switch to the non-privileged user to run the application.
# USER appuser

# Copy the source code into the container.
COPY . /app

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
