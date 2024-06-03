# MobileX Experience Lab - Backend

## Requirements

- Poetry: `pip install poetry`

## Debug on my Local machine

```bash
# Install dependencies
poetry install --all-extras

# Run!
fastapi dev main.py
```

## Build a Container image

```bash
tar -czh . | docker build --tag docker.io/{my docker account name}/{my image name}:{version} -
docker push docker.io/{my docker account name}/{my image name}:{version}

# Example:
tar -czh . | docker build --tag docker.io/kerryeon/mobilex-exp-backend:v0.1 -
docker push docker.io/kerryeon/mobilex-exp-backend:v0.1
```

### Build with buildx

```bash
tar -czh . | docker buildx build --push --pull --tag docker.io/{my docker account name}/{my image name}:{version} -

# Example:
tar -czh . | docker buildx build --push --pull --tag docker.io/kerryeon/mobilex-exp-backend:v0.1 -
```

## Dump OpenAPI Schema for other languages

It is convenient to use the `OpenAPI` format when calling backend services from other languages and frameworks such as cURL, Flutter, Java, and Rust.
`OpenAPI` is a format that creates a language-neutral API call schema.
Popular languages and frameworks support converting `OpenAPI` schema into native language and framework code for your environment.

```bash
# Run development server *OR* use production server
fastapi dev main.py

# On the browser: open and download your OpenAPI schema
open "http://localhost:8000/openapi.json"
```
