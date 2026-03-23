import pandas as pd
import os

def main():
    input_file = "backend/data/arboles-madrid.xlsx"
    output_file = "backend/data/arboles-madrid.csv"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Reading {input_file}...")
    # Read the Excel file
    df = pd.read_excel(input_file)
    print(f"Read {len(df)} rows.")

    print(f"Writing to {output_file}...")
    # Save to CSV
    df.to_csv(output_file, index=False)
    print("Done!")

if __name__ == "__main__":
    main()
