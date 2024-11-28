import serial 
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import time

# UART configuration (adjust the port if necessary)
UART_PORT = '/dev/ttyACM0' # On Pi, GPIO 14 (TX) and 15 (RX)
UART_BAUDRATE = 115200

# InfluxDB configuration
INFLUXDB_URL = "http://localhost:8086"  # Update if using a remote uartver
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
    Process the UART data line into InfluxDB format.
    """
    try:
        # Each line should already be in InfluxDB line protocol format
        if data_line:
            send_to_influxdb(data_line)
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
        # Read available data
        time.sleep(0.5)
if __name__ == "__main__":
    main()
