FROM python:3.12

# Install poetry
RUN pip install poetry

# Set up working directory
WORKDIR /app

# Copy poetry files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-root


# Set up source code
COPY . .

# Change working directory to the source code directory
WORKDIR src

# Command to run the server
CMD ["poetry", "run", "gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
