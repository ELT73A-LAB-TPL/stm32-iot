import os
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

# --- InfluxDB Connection Details ---
# IMPORTANT: Replace these with the actual values from your .env file or your InfluxDB setup.
# For a production environment, you would typically load these from environment variables
# or a secure configuration management system.
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "mytoken"  # Replace with your INFLUXDB_TOKEN
INFLUXDB_ORG = "IoT"        # Replace with your DOCKER_INFLUXDB_INIT_ORG
INFLUXDB_BUCKET = "Node-RED" # Replace with your DOCKER_INFLUXDB_INIT_BUCKET

def test_influxdb_connection():
    """
    Connects to InfluxDB, writes a sample data point, and then queries it back.
    """
    print(f"Attempting to connect to InfluxDB at: {INFLUXDB_URL}")
    print(f"Using Organization: {INFLUXDB_ORG}, Bucket: {INFLUXDB_BUCKET}")

    try:
        # Initialize InfluxDB client
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

        # --- Write Data ---
        # Get the synchronous write API
        write_api = client.write_api(write_options=SYNCHRONOUS)

        # Create a data point
        # This point represents a "temperature" measurement from "sensor_01" in "room_a"
        # with a value of 25.5 degrees Celsius.
        point = Point("temperature") \
            .tag("sensor_id", "sensor_01") \
            .tag("room", "room_a") \
            .field("value", 25.5) \
            .time(datetime.datetime.utcnow(), datetime.timezone.utc) # Use UTC for consistency

        print("\nWriting sample data point...")
        write_api.write(bucket=INFLUXDB_BUCKET, record=point)
        print("Data point written successfully!")
        print(f"  Measurement: {point.get_measurement_name()}")
        print(f"  Tags: {point.get_tags()}")
        print(f"  Fields: {point.get_fields()}")
        print(f"  Timestamp: {point.get_time()}")


        # --- Query Data ---
        query_api = client.query_api()

        # Flux query to retrieve the data we just wrote
        # This query selects all data from the specified bucket,
        # filters by measurement "temperature", and limits to the last 10 minutes.
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
          |> range(start: -10m)
          |> filter(fn: (r) => r._measurement == "temperature")
          |> filter(fn: (r) => r.sensor_id == "sensor_01")
        '''

        print("\nQuerying data...")
        tables = query_api.query(query, org=INFLUXDB_ORG)

        found_data = False
        for table in tables:
            for record in table.records:
                found_data = True
                print(f"  Retrieved Record:")
                print(f"    Time: {record.get_time()}")
                print(f"    Measurement: {record.get_measurement()}")
                print(f"    Field: {record.get_field()}")
                print(f"    Value: {record.get_value()}")
                print(f"    Sensor ID: {record['sensor_id']}")
                print(f"    Room: {record['room']}")
                print("-" * 20)

        if not found_data:
            print("No data found matching the query in the last 10 minutes. This might indicate an issue or a delay in data visibility.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure InfluxDB is running and accessible at the specified URL,")
        print("and that your token, organization, and bucket are correct.")
    finally:
        # Close the client connection
        if 'client' in locals() and client:
            client.close()
            print("\nInfluxDB client connection closed.")

if __name__ == "__main__":
    test_influxdb_connection()
