# Madrid Routing App — Backend

FastAPI server for the Madrid Routing App.

## Setup

1. (Optional) Create an environment file:
   ```bash
   cp .env.example .env
   ```

2. Run the server using `uv`:
   ```bash
   # From the project root
   uv run uvicorn backend.main:app --reload
   ```

## API Endpoints

- `GET /health`: Check if the server is running.
- `POST /route`: Get a mock GeoJSON route (straight line).
- `POST /summary`: Generate a human-friendly journey description.
