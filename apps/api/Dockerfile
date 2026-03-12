FROM python:3.11-slim

WORKDIR /workspace

COPY pyproject.toml /workspace/pyproject.toml
COPY apps /workspace/apps
COPY jobs /workspace/jobs
COPY packages /workspace/packages
COPY config /workspace/config
COPY docs /workspace/docs
COPY migrations /workspace/migrations
COPY scripts /workspace/scripts

RUN pip install --no-cache-dir -e .

CMD ["uvicorn", "apps.api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

