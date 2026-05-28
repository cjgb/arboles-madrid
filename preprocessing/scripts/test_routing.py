import httpx
import random
import time
import sys

# Base URL for the running backend
BASE_URL = "http://localhost:8000"

# Sample points in Madrid [lon, lat]
MADRID_POINTS = [
    [-3.7038, 40.4168], # Sol
    [-3.6827, 40.4150], # Retiro
    [-3.7122, 40.4239], # Plaza de España
    [-3.6883, 40.4235], # Serrano
    [-3.7058, 40.4464], # Santiago Bernabéu
    [-3.7105, 40.4070], # Embajadores
    [-3.6695, 40.4300], # Ventas
    [-3.7250, 40.4350], # Moncloa
    [-3.6800, 40.4500], # Chamartín
    [-3.6500, 40.4100], # Moratalaz
]

def test_health():
    print("Checking backend health...")
    try:
        # Increase timeout to 60s
        response = httpx.get(f"{BASE_URL}/health", timeout=60.0)
        if response.status_code == 200:
            data = response.json()
            print(f"Health OK: {data}")
            return data.get("graph_loaded", False)
        else:
            print(f"Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return False

def test_random_routes(n=10):
    print(f"\nRunning {n} random routing tests...")
    success_count = 0
    
    for i in range(n):
        start = random.choice(MADRID_POINTS)
        end = random.choice(MADRID_POINTS)
        while end == start:
            end = random.choice(MADRID_POINTS)
            
        print(f"Test {i+1}: Route from {start} to {end}...")
        
        try:
            payload = {
                "start": start,
                "end": end,
                "profile": "driving-car"
            }
            start_time = time.time()
            response = httpx.post(f"{BASE_URL}/route", json=payload, timeout=30.0)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                features = data.get("features", [])
                if features:
                    feat = features[0]
                    dist = feat["properties"]["segments"][0]["distance"]
                    coords_count = len(feat["geometry"]["coordinates"])
                    print(f"  SUCCESS: {dist:.1f}m, {coords_count} nodes, {elapsed:.2f}s")
                    success_count += 1
                    
                    # Also test summary endpoint
                    summary_payload = {
                        "distance_km": dist / 1000,
                        "duration_min": feat["properties"]["segments"][0]["duration"] / 60,
                        "start_name": "Point A",
                        "end_name": "Point B"
                    }
                    sum_res = httpx.post(f"{BASE_URL}/summary", json=summary_payload)
                    if sum_res.status_code == 200:
                        print(f"  Summary: {sum_res.json()['summary']}")
                else:
                    print(f"  FAILED: No features in response")
            else:
                print(f"  FAILED: Status {response.status_code}, {response.text}")
                
        except Exception as e:
            print(f"  ERROR: {e}")
            
    print(f"\nResults: {success_count}/{n} routes successful.")
    return success_count == n

if __name__ == "__main__":
    if not test_health():
        print("Backend not ready or graph not loaded. Please start 'uv run uvicorn backend.main:app --port 8000' first.")
        sys.exit(1)
        
    if test_random_routes(10):
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)
