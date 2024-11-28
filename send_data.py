import requests
import json
from datetime import datetime

# Firebase configuration from Step 3
firebase_url = "https://spartan-concord-413207-default-rtdb.asia-southeast1.firebasedatabase.app"  # Replace with your Firebase database URL

# Function to send sensor data to Firebase
def send_to_firebase(sensor_name, sensor_value):
    timestamp = datetime.now().isoformat()  # Current timestamp in ISO format
    data = {
        "timestamp": timestamp,
        "sensor_name": sensor_name,
        "sensor_value": sensor_value
    }
    
    # Send data to Firebase Realtime Database
    response = requests.post(firebase_url + "/sensor_data.json", data=json.dumps(data))
    
    if response.status_code == 200:
        print("Data sent to Firebase successfully!")
    else:
        print("Failed to send data:", response.status_code, response.text)

# Example: Reading sensor data from Pico
# Assuming data comes in the format {'sensor_name': 'Temperature', 'sensor_value': 23.4}
# Replace this example with actual data retrieval from your Pico
sensor_name = "Temperature"
sensor_value = 23.4

# Send data to Firebase
send_to_firebase(sensor_name, sensor_value)
