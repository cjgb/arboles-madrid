#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo ">>> Starting preprocessing pipeline..."

# Ensure directories exist
mkdir -p preprocessing/data
mkdir -p backend/data

# List of scripts to run in order
SCRIPTS=(
    "to_csv.py"
    "download_osm.py"
    "create_network.py"
    "blend_networks.py"
    "optimize_graph.py"
)

for script in "${SCRIPTS[@]}"; do
    echo ""
    echo ">>> Running $script..."
    python "preprocessing/scripts/$script"
done

# Copy the final optimized graph to the backend
SRC_PKL="preprocessing/data/blended_network.pkl"
DEST_PKL="backend/data/blended_network.pkl"

if [ -f "$SRC_PKL" ]; then
    echo ""
    echo ">>> Copying $SRC_PKL to $DEST_PKL..."
    cp "$SRC_PKL" "$DEST_PKL"
    echo "Done! The backend is now ready to serve the updated data."
else
    echo ""
    echo "Error: $SRC_PKL was not generated."
    exit 1
fi
