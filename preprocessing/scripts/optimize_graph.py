import os
import pickle
import networkx as nx
from scipy.spatial import KDTree
import time

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "data", "blended_network.graphml")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "blended_network.pkl")

def optimize_graph():
    if not os.path.exists(INPUT_PATH):
        print(f"Error: No se encontró el archivo {INPUT_PATH}")
        return

    print(f"Paso 1: Cargando el grafo pesado (esto puede tardar unos minutos y mucha RAM)...")
    start_time = time.time()
    G = nx.read_graphml(INPUT_PATH)
    print(f"Grafo cargado: {G.number_of_nodes()} nodos, {G.number_of_edges()} edges en {time.time() - start_time:.2f} segundos.")

    print("Paso 2: Limpiando atributos innecesarios para ahorrar memoria...")
    # Node attributes to keep
    NODE_KEEP = {'x', 'y', 'type'}
    # Edge attributes to keep
    EDGE_KEEP = {'weight', 'length', 'type'}

    # Process nodes
    node_coords = []
    nodes_list = []
    for n, d in G.nodes(data=True):
        # Keep only essential attributes and ensure correct types
        to_delete = [k for k in d if k not in NODE_KEEP]
        for k in to_delete:
            del d[k]
        
        # Ensure x and y are floats for calculations
        if 'x' in d and 'y' in d:
            x, y = float(d['x']), float(d['y'])
            d['x'] = x
            d['y'] = y
            node_coords.append([x, y])
            nodes_list.append(n)

    # Process edges
    for u, v, d in G.edges(data=True):
        to_delete = [k for k in d if k not in EDGE_KEEP]
        for k in to_delete:
            del d[k]
        
        # Ensure length and weight are floats (important for shortest path)
        if 'length' in d:
            d['length'] = float(d['length'])
        if 'weight' in d:
            d['weight'] = float(d['weight'])

    print("Paso 3: Construyendo el KDTree...")
    kdtree = KDTree(node_coords)
    print("KDTree listo.")

    print(f"Paso 4: Guardando en formato binario ({OUTPUT_PATH})...")
    data = {
        'G': G,
        'kdtree': kdtree,
        'nodes_list': nodes_list
    }
    
    with open(OUTPUT_PATH, 'wb') as f:
        # Using a high protocol for performance and compression
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(f"¡Éxito! El grafo optimizado se ha guardado.")
    print(f"Tiempo total: {time.time() - start_time:.2f} segundos.")

if __name__ == "__main__":
    optimize_graph()
