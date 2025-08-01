# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.10

# Set up the application directory
ENV APP_HOME /app
ENV VENV_PATH /opt/venv
WORKDIR /app

# Install poetry
RUN pip install 'poetry==1.3.2'

# Copy only the files needed for dependency installation
COPY backend/python/pyproject.toml backend/python/poetry.lock ./

# Copy the Python source code
COPY backend/python/services ./services
COPY backend/python/main.py ./

# Copy synthea data from project root
COPY synthea ./synthea

# Configure poetry to not create a virtual environment (we'll use system Python)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

EXPOSE 8000

# Development mode with hot reload
CMD exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app
