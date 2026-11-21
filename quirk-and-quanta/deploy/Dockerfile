# Quirk & Quanta - Production Cloud Run / Container Dockerfile
# Zero external dependencies: Uses Python Standard Library exclusively.
# Workshop: "Beyond Basic RAG: Building Production-Ready AI Systems"

FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Create secure non-root system user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/false -m appuser

WORKDIR /app

# Copy application directories and files
COPY site /app/site
COPY data /app/data
COPY rag /app/rag
COPY scripts /app/scripts

# Fix ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 8080 8000

# Health check using Python standard library on /health
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import os, urllib.request; p = os.environ.get('PORT', '8080'); urllib.request.urlopen(f'http://localhost:{p}/health', timeout=3)" || exit 1

# Launch unified server (reads PORT dynamically from environment or defaults to 8080/8000)
CMD ["python3", "rag/server.py"]
