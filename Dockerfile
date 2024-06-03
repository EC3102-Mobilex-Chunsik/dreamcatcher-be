# Configure metadata
ARG POETRY_VERSION="1.3.2"
ARG PYTHON_VERSION="3.12"
ARG PYTHON_DIST="bookworm"

# --- builder ----
FROM "docker.io/library/python:${PYTHON_VERSION}-${PYTHON_DIST}" as builder

# Configure poetry environment variables
ARG POETRY_CACHE_DIR=/tmp/poetry_cache
ENV POETRY_NO_INTERACTION=1
ARG POETRY_VERSION
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1

# Install poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Load package metadata
WORKDIR /app

COPY pyproject.toml ./

# Install package dependencies
RUN --mount=type=cache,target=${POETRY_CACHE_DIR} \
    poetry install --no-root --without dev
# openai migrate 명령을 실행하여 코드베이스를 새로운 openai API로 마이그레이션
# RUN openai migrate

# --- runtime ----
FROM "docker.io/library/python:${PYTHON_VERSION}-slim-${PYTHON_DIST}" as runtime

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Configure entrypoint
ENTRYPOINT ["/usr/bin/env"]
CMD [ "fastapi", "run", "main.py" ]

# Configure runtime environment variables
ENV PATH="/app/.venv/bin:${PATH}"

# Load package source codes
WORKDIR /app
COPY --from=builder /app/.venv .venv
ADD ./ .
