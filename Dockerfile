FROM python:3.11-slim

# Install uv (package manager)
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ ./src/

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uv", "run", "uvicorn", "src.endpoint.main:app", "--host", "0.0.0.0", "--port", "8000"]
