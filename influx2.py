import serial
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import time

# UART configuration (adjust the port if necessary)
UART_PORT = '/dev/ttyACM0'  # On Pi, GPIO 14 (TX) and 15 (RX)
UART_BAUDRATE = 115200

# InfluxDB configuration
INFLUXDB_URL = "http://localhost:8086"  # Update if using a remote server
INFLUXDB_TOKEN = "L0ZXOxNyGZfQYS3fm2E5VXF9wtBuUvQ2lygXqrBa_4Rhc4ahaQvqw7Y212PXMj5wdXhLz0rPH-9AvAQSaXpVOg=="
INFLUXDB_ORG = "bmsce"
INFLUXDB_BUCKET = "incubator/sensor"

# Initialize UART
uart = serial.Serial(UART_PORT, baudrate=UART_BAUDRATE, timeout=1)

# Initialize InfluxDB client
influx_client = influxdb_client.InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def send_to_influxdb(data):
    """
    Send formatted data to InfluxDB.
    """
    try:
        write_api.write(bucket=INFLUXDB_BUCKET, record=data)
        print("Data sent to InfluxDB successfully.")
    except Exception as e:
        print(f"Failed to send data to InfluxDB: {e}")

def process_uart_data(data_line):
    """
    Process the UART data line into InfluxDB line protocol format.
    """
    try:
        # Example incoming JSON-like data: {"temperature": 26.3, "humidity": 55.4, "light_level": 9.73}
        sensor_data = eval(data_line)  # Use `json.loads` if input is proper JSON
        measurement = "incubator_data"
        
        # Prepare line protocol
        fields = [
            f"temperature={sensor_data['temperature']}",
            f"humidity={sensor_data['humidity']}",
            f"light_level={sensor_data['light_level']}"
        ]
        if "heart_rate_voltage" in sensor_data:
            fields.append(f"heart_rate_voltage={sensor_data['heart_rate_voltage']}")
        if "object_temp" in sensor_data:
            fields.append(f"object_temp={sensor_data['object_temp']}")
        
        # Construct the line protocol
        line_protocol = f"{measurement} {','.join(fields)}"
        print(f"Formatted line protocol: {line_protocol}")
        
        # Send to InfluxDB
        send_to_influxdb(line_protocol)
    except Exception as e:
        print(f"Error processing data: {e}")

def main():
    """
    Main loop to read data from UART and send to InfluxDB.
    """
    print("Starting UART to InfluxDB script...")
    while True:
        data_line = uart.readline().decode("utf-8").strip()
        print(f"Received data: {data_line}")
        
        # Process and send the data to InfluxDB
        process_uart_data(data_line)
        
        # Delay to control data ingestion rate
        time.sleep(0.5)

if __name__ == "__main__":
    main()
