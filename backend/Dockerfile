# Use a specialized uv image for building
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the uv configuration files from the root
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
RUN uv sync --frozen --no-dev

# Use a clean, smaller final image
FROM python:3.13-slim-bookworm

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy the backend source code and data
COPY backend/ /app/backend/

# Ensure the virtual environment is used
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Run the application
WORKDIR /app/backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
