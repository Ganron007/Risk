# syntax=docker/dockerfile:1
FROM python:3.11-slim

LABEL maintainer="CADRE Platform <https://github.com/Ganron007/CADRE>"
LABEL description="CADRE-Risk — CISSP-aligned GRC risk scoring, board memos, and unified dashboard"

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8895 \
    HOST=0.0.0.0

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy package metadata and install python dependencies
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/
RUN pip install --no-cache-dir -e ".[dev,live]"

# Copy configuration, samples, assets, and docs
COPY config/ ./config/
COPY samples/ ./samples/
COPY docs/ ./docs/
COPY assets/ ./assets/

# Pre-generate baseline artifacts
RUN mkdir -p artifacts && \
    python -c "from src.server import refresh_artifacts; refresh_artifacts()"

EXPOSE 8895

CMD ["python", "-m", "src.server"]
