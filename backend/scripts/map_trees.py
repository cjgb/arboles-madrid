import pandas as pd
import folium
from folium.plugins import FastMarkerCluster
from pyproj import Transformer
import os

def main():
    file_path = "backend/data/arboles-madrid.xlsx"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    print(f"Reading all data from {file_path}...")
    # Reading 793k rows from Excel can take a minute and significant RAM.
    df = pd.read_excel(file_path, usecols=['X', 'Y'])
    print(f"Read {len(df)} rows.")

    print("Transforming all coordinates (UTM 30N -> WGS84)...")
    # EPSG:25830 is ETRS89 / UTM zone 30N
    transformer = Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)
    
    # Vectorized transformation for speed
    lon, lat = transformer.transform(df['X'].values, df['Y'].values)
    
    # Create a list of [lat, lon] directly to save memory
    print("Preparing coordinate list...")
    data = list(zip(lat, lon))
    
    # Clear df to free memory
    del df

    print("Generating map with FastMarkerCluster...")
    # Center on Madrid
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=11, tiles="CartoDB positron")

    # FastMarkerCluster is optimized for hundreds of thousands of points
    FastMarkerCluster(data, name="Todos los árboles").add_to(m)

    output_file = "web/index.html"
    print(f"Saving map to {output_file} (this may take a moment)...")
    m.save(output_file)
    print("Done!")

if __name__ == "__main__":
    main()
