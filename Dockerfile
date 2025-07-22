# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project definition files and source code
COPY pyproject.toml ./
COPY config ./config
COPY src ./src
COPY scripts ./scripts

# Install dependencies without development packages
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Expose ports for API and metrics
EXPOSE 8000 8001

# Default command to run the API server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
