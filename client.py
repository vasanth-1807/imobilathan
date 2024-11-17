import random
import time
import requests

def generate_vehicle_data(vehicle_id):
    return {
        "vehicle_id": vehicle_id,
        "location": "Route_Salem_Coimbatore",
        "speed": round(random.uniform(40, 80), 2),
        "road_condition": random.choice(["Good", "Moderate", "Poor"]),
        "weather": random.choice(["Clear", "Rainy", "Foggy"]),
        "timestamp": time.time()
    }

def send_data(vehicle_id, server_url):
    while True:
        data = generate_vehicle_data(vehicle_id)
        try:
            response = requests.post(f"{server_url}/send_data", json=data)
            if response.status_code == 200:
                print(f"[{vehicle_id}] Data sent successfully: {data}")
            else:
                print(f"[{vehicle_id}] Failed to send data")
        except Exception as e:
            print(f"[{vehicle_id}] Error: {e}")
        time.sleep(random.randint(3, 5))

if __name__ == '__main__':
    # Example vehicle IDs
    vehicle_ids = [f"Car_{i}" for i in range(1, 6)]
    server_url = "http://127.0.0.1:5000"

    # Start sending data for each vehicle
    for vehicle_id in vehicle_ids:
        send_data(vehicle_id, server_url)
