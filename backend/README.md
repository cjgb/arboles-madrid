# Madrid Routing App — Backend

FastAPI server for the Madrid Routing App.

## Data

The backend requires an optimized graph file at `backend/data/blended_network.pkl`. 
If this file is missing, you must generate it using the preprocessing tools.

## Preprocessing

To (re)generate the routing data:

1. Ensure you have the raw data (`.xlsx`) in `preprocessing/data/`.
2. Run the orchestrator script from the project root:
   ```bash
   bash preprocessing/process_data.sh
   ```
   This will download OSM data, process trees, blend the networks, and copy the final `.pkl` to the backend.

## Running the API

```bash
# From the project root
uv run uvicorn backend.main:app --reload
```

## API Endpoints

- `GET /health`: Check if the server is running and the graph is loaded.
- `POST /route`: Calculate the optimal route between two points using the blended network.
- `POST /summary`: Generate a human-friendly journey description.
