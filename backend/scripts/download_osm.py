import osmnx as ox
import os

def main():
    place_name = "Madrid, Spain"
    output_file = "backend/data/madrid_network.graphml"
    
    if os.path.exists(output_file):
        print(f"File {output_file} already exists. Skipping download.")
        return

    print(f"Downloading road network for {place_name}...")
    # Get the road network (drive, bike, walk, or all)
    # instructions mention "road grid", let's use 'drive' as a standard
    try:
        # Instead of all of Madrid, let's get a generous area around the center
        # to keep it manageable but useful for routing.
        # lat: 40.4168, lon: -3.7038
        G = ox.graph_from_point((40.4168, -3.7038), dist=10000, network_type='drive')
        
        print(f"Saving network to {output_file}...")
        ox.save_graphml(G, output_file)
        print("Done!")
    except Exception as e:
        print(f"Error downloading OSM data: {e}")

if __name__ == "__main__":
    main()
