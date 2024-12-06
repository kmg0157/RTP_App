from GPS_Rec import GPSReader
from client import Client
import time
import json  # Import the missing module

def main():
    gps_data = GPSReader()  # GPS reader object
    sender = Client()

    print("Application started!")
    sender.accept()  # Establish server connection

    try:
        while True:
            data = gps_data.read_data()  # Fetch GPS data

            # Process and save data if available
            if data:
                sender.run_client(json.dumps(data).encode('utf-8'))  # Serialize and send GPS data

                # Print received data
                print(
                    f"Sequence: {data.get('Sequence')}, "
                    f"Timestamp: {data.get('Timestamp')}, "
                    f"Latitude: {data.get('Latitude')}, "
                    f"Longitude: {data.get('Longitude')}"
                )

                time.sleep(3)

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Inform server and close resources
        sender.run_client("CLOSE".encode('utf-8'))
        sender.close()  # This now exists in the Client class
        print("Application terminated.")

if __name__ == "__main__":
    main()
