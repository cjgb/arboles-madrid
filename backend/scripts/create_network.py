import pandas as pd
import numpy as np
from scipy.spatial import KDTree
import os

def main():
    input_file = "backend/data/arboles-madrid.csv"
    output_file = "backend/data/tree_network.csv"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Reading {input_file}...")
    # Use only necessary columns to save memory
    df = pd.read_csv(input_file, usecols=['ASSETNUM', 'X', 'Y', 'ALTURA_TOTAL'])
    # Fill NaN heights with the mean to avoid issues in the formula
    df['ALTURA_TOTAL'] = df['ALTURA_TOTAL'].fillna(df['ALTURA_TOTAL'].mean())
    print(f"Read {len(df)} rows.")

    # Convert coordinates to a numpy array for KDTree
    coords = df[['X', 'Y']].values
    heights = df['ALTURA_TOTAL'].values
    ids = df['ASSETNUM'].values

    print("Building KDTree...")
    tree = KDTree(coords)

    # Maximum possible height is around 45m (ignoring outliers)
    # R_max = 2 + (45 + 45) / 3 = 32m
    # Let's use 35m as a safe search radius for the KDTree
    search_radius = 35.0

    print(f"Finding pairs within {search_radius}m radius...")
    # query_pairs returns a set of (i, j) index pairs
    pairs = tree.query_pairs(r=search_radius)
    print(f"Found {len(pairs)} candidate pairs.")

    print("Filtering pairs by the specific formula...")
    network_data = []
    
    # Formula: distance < 2 + (height1 + height2) / 3
    # We need the actual distance for each pair
    count = 0
    for i, j in pairs:
        dist = np.sqrt(np.sum((coords[i] - coords[j])**2))
        h1 = heights[i]
        h2 = heights[j]
        
        if dist < 2 + (h1 + h2) / 3:
            network_data.append({
                'tree_id_1': ids[i],
                'tree_id_2': ids[j],
                'distance': round(dist, 2),
                'height_1': h1,
                'height_2': h2
            })
        
        count += 1
        if count % 100000 == 0:
            print(f"Processed {count} pairs...")

    print(f"Found {len(network_data)} valid links in the network.")
    
    network_df = pd.DataFrame(network_data)
    print(f"Writing network to {output_file}...")
    network_df.to_csv(output_file, index=False)
    print("Done!")

if __name__ == "__main__":
    main()
