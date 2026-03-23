import pandas as pd
import folium
from pyproj import Transformer
import os

def main():
    tree_file = "backend/data/arboles-madrid.csv"
    network_file = "backend/data/tree_network.csv"
    output_file = "web/network_map.html"

    if not os.path.exists(tree_file) or not os.path.exists(network_file):
        print("Error: Required CSV files not found. Run to_csv.py and create_network.py first.")
        return

    print("Reading tree data and network...")
    # Use only necessary columns to keep memory usage low
    trees = pd.read_csv(tree_file, usecols=['ASSETNUM', 'X', 'Y'])
    network = pd.read_csv(network_file, usecols=['tree_id_1', 'tree_id_2'])
    
    print(f"Loaded {len(network)} links.")

    # Transform coordinates
    print("Transforming coordinates (UTM 30N -> WGS84)...")
    transformer = Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(trees['X'].values, trees['Y'].values)
    trees['lat'] = lat
    trees['lon'] = lon
    
    # Create a mapping of ASSETNUM to (lat, lon)
    # Using a dictionary for O(1) lookups
    coords_dict = dict(zip(trees['ASSETNUM'].astype(int), zip(trees['lat'], trees['lon'])))
    
    # Free up tree dataframe memory
    del trees

    print("Preparing all segments for the map...")
    segments = []
    # Vectorized or fast iteration to build the segments list
    for id1, id2 in zip(network['tree_id_1'].astype(int), network['tree_id_2'].astype(int)):
        if id1 in coords_dict and id2 in coords_dict:
            segments.append([coords_dict[id1], coords_dict[id2]])

    print("Generating map...")
    # Center on Madrid
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=12, tiles="CartoDB positron")

    print(f"Adding {len(segments)} segments to the map (this will create a very large HTML file)...")
    # MultiPolyLine is the most efficient standard way in Folium/Leaflet for this
    folium.PolyLine(
        locations=segments,
        color="black",
        weight=0.5, # Thinner lines for higher density
        opacity=0.4 # Higher transparency to better see clusters
    ).add_to(m)

    print(f"Saving map to {output_file}...")
    m.save(output_file)
    print(f"Done! {output_file} generated.")

if __name__ == "__main__":
    main()
