import osmnx as ox
import networkx as nx
import pandas as pd
import numpy as np
from pyproj import Transformer
import os
from tqdm import tqdm

def main():
    osm_file = "backend/data/madrid_network.graphml"
    tree_file = "backend/data/arboles-madrid.csv"
    network_file = "backend/data/tree_network.csv"
    output_file = "backend/data/blended_network.graphml"

    if not all(os.path.exists(f) for f in [osm_file, tree_file, network_file]):
        print("Error: Missing required files.")
        return

    print("Loading OSM graph...")
    G_osm = ox.load_graphml(osm_file)
    print("Converting to undirected...")
    G_osm = ox.convert.to_undirected(G_osm)
    
    print("Pre-processing OSM edges...")
    for u, v, data in G_osm.edges(data=True):
        data['weight'] = data.get('length', 0)
        keys_to_remove = [k for k in data if k not in ['weight', 'length']]
        for k in keys_to_remove:
            del data[k]

    print("Loading tree data and network...")
    trees_df = pd.read_csv(tree_file, usecols=['ASSETNUM', 'X', 'Y'])
    # Drop duplicates to ensure unique index for to_dict
    trees_df = trees_df.drop_duplicates(subset=['ASSETNUM'])
    network_df = pd.read_csv(network_file)

    print("Transforming tree coordinates...")
    transformer = Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(trees_df['X'].values, trees_df['Y'].values)
    trees_df['lon'] = lon
    trees_df['lat'] = lat

    # Create a lookup for tree coordinates
    tree_coords = trees_df.set_index('ASSETNUM')[['lon', 'lat']].to_dict('index')

    print("Blending networks...")
    G_blended = nx.Graph(G_osm)
    
    network_trees = pd.unique(network_df[['tree_id_1', 'tree_id_2']].values.ravel('K'))
    print(f"Adding {len(network_trees)} tree nodes to the graph...")

    for tree_id in tqdm(network_trees, desc="Adding tree nodes"):
        if tree_id in tree_coords:
            coords = tree_coords[tree_id]
            G_blended.add_node(f"tree_{int(tree_id)}", x=coords['lon'], y=coords['lat'], type='tree')

    print("Adding tree-to-tree edges (weight 0)...")
    for _, row in tqdm(network_df.iterrows(), total=len(network_df), desc="Adding tree edges"):
        u = f"tree_{int(row['tree_id_1'])}"
        v = f"tree_{int(row['tree_id_2'])}"
        if G_blended.has_node(u) and G_blended.has_node(v):
            G_blended.add_edge(u, v, weight=0, length=row['distance'], type='tree_link')

    print("Connecting tree network to OSM network...")
    tree_ids_in_network = [tid for tid in network_trees if tid in tree_coords]
    lons = [tree_coords[tid]['lon'] for tid in tree_ids_in_network]
    lats = [tree_coords[tid]['lat'] for tid in tree_ids_in_network]

    print("Finding nearest OSM nodes for all trees (this may take a minute)...")
    nearest_osm_nodes = ox.distance.nearest_nodes(G_osm, lons, lats)

    for tree_id, osm_node in tqdm(zip(tree_ids_in_network, nearest_osm_nodes), total=len(tree_ids_in_network), desc="Connecting trees to OSM"):
        tree_node_id = f"tree_{int(tree_id)}"
        if G_blended.has_node(tree_node_id):
            # Calculate physical distance between the tree and the nearest OSM node
            t_lon = tree_coords[tree_id]['lon']
            t_lat = tree_coords[tree_id]['lat']
            osm_node_data = G_osm.nodes[osm_node]
            osm_lon = osm_node_data['x']
            osm_lat = osm_node_data['y']
            
            # Distance in meters
            dist = ox.distance.great_circle(t_lat, t_lon, osm_lat, osm_lon)
            
            # Use real distance for weight and length for connectors
            G_blended.add_edge(tree_node_id, osm_node, weight=dist, length=dist, type='connector')

    print(f"Final graph has {G_blended.number_of_nodes()} nodes and {G_blended.number_of_edges()} edges.")
    
    print(f"Saving blended graph to {output_file}...")
    nx.write_graphml(G_blended, output_file)
    print("Done!")

if __name__ == "__main__":
    main()
