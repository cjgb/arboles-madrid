import os
import pickle
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import networkx as nx
from scipy.spatial import KDTree
import numpy as np
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for the graph and KDTree
G = None
nodes_list = []
kdtree = None

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_PATH_PKL = os.path.join(BASE_DIR, "data", "blended_network.pkl")
GRAPH_PATH_XML = os.path.join(BASE_DIR, "data", "blended_network.graphml")

def load_graph():
    global G, nodes_list, kdtree
    
    if os.path.exists(GRAPH_PATH_PKL):
        print(f"Loading optimized binary graph from {GRAPH_PATH_PKL}...")
        with open(GRAPH_PATH_PKL, 'rb') as f:
            data = pickle.load(f)
            G = data['G']
            kdtree = data['kdtree']
            nodes_list = data['nodes_list']
        print(f"Graph loaded successfully from binary: {G.number_of_nodes()} nodes.")
        return

    if os.path.exists(GRAPH_PATH_XML):
        print(f"Optimized binary not found. Loading from GraphML {GRAPH_PATH_XML}...")
        G = nx.read_graphml(GRAPH_PATH_XML)
        print(f"Graph loaded from XML: {G.number_of_nodes()} nodes.")
        
        # Pre-process on the fly
        node_coords = []
        for n, d in G.nodes(data=True):
            if 'x' in d and 'y' in d:
                x, y = float(d['x']), float(d['y'])
                G.nodes[n]['x'] = x
                G.nodes[n]['y'] = y
                node_coords.append([x, y])
                nodes_list.append(n)
        
        if node_coords:
            kdtree = KDTree(node_coords)
            print("KDTree built successfully.")
    else:
        print(f"Warning: Neither {GRAPH_PATH_PKL} nor {GRAPH_PATH_XML} found. Routing will fail.")

# Load data on start
load_graph()

class RouteRequest(BaseModel):
    start: List[float]  # [lon, lat]
    end: List[float]    # [lon, lat]
    profile: str = "driving-car"

class SummaryRequest(BaseModel):
    distance_km: float
    duration_min: float
    start_name: str
    end_name: str

@app.get("/health")
async def health():
    return {"status": "ok", "graph_loaded": G is not None}

@app.post("/route")
async def get_route(request: RouteRequest):
    if G is None or kdtree is None:
        raise HTTPException(status_code=500, detail="Blended graph or KDTree not loaded")

    lon1, lat1 = request.start
    lon2, lat2 = request.end

    try:
        # Use KDTree for nearest node search (handles any node ID type)
        _, start_idx = kdtree.query([lon1, lat1])
        _, end_idx = kdtree.query([lon2, lat2])
        
        start_node = nodes_list[start_idx]
        end_node = nodes_list[end_idx]

        # Calculate the shortest path by weight
        shortest_path = nx.shortest_path(G, start_node, end_node, weight='weight')
        
        path_coords = []
        tree_points = []
        total_distance_m = 0
        tree_distance_m = 0
        road_distance_m = 0
        tree_hops = 0
        
        for i in range(len(shortest_path)):
            u = shortest_path[i]
            node_data = G.nodes[u]
            u_coords = [float(node_data['x']), float(node_data['y'])]
            path_coords.append(u_coords)
            
            # Identify if the node is a tree
            if node_data.get('type') == 'tree':
                tree_points.append(u_coords)

            # Process edges for distance and hop counts
            if i < len(shortest_path) - 1:
                v = shortest_path[i+1]
                edge_data = G.get_edge_data(u, v)
                
                # length might be a string if loaded from graphml
                length = float(edge_data.get('length', 0))
                edge_type = edge_data.get('type')

                total_distance_m += length
                
                if edge_type == 'tree_link':
                    tree_distance_m += length
                    tree_hops += 1
                elif edge_type == 'connector':
                    tree_distance_m += length
                else:
                    # Standard road edge
                    road_distance_m += length

        # Estimate duration: 40 km/h
        total_duration_sec = total_distance_m / 11.11

        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "segments": [
                            {
                                "distance": total_distance_m,
                                "duration": total_duration_sec,
                                "tree_distance": tree_distance_m,
                                "road_distance": road_distance_m,
                                "tree_hops": tree_hops,
                                "steps": []
                            }
                        ],
                        "summary": {
                            "distance": total_distance_m,
                            "duration": total_duration_sec
                        },
                        "tree_points": tree_points
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": path_coords
                    }
                }
            ]
        }
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No route found between points")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summary")
async def get_summary(request: SummaryRequest):
    summary = (
        f"El trayecto desde {request.start_name} hasta {request.end_name} "
        f"recorre {request.distance_km:.1f} km."
    )
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
