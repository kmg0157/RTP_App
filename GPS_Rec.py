from gps3 import gps3

class GPSReader:
    def __init__(self):
        self.gps_socket = gps3.GPSDSocket()
        self.data_stream = gps3.DataStream()
        self.gps_socket.connect()
        self.gps_socket.watch()
        self.sequence = 0

    def read_data(self):
        """Read and process GPS data."""
        try:
            for new_data in self.gps_socket:
                if new_data:
                    self.data_stream.unpack(new_data)
                    latitude = self.data_stream.TPV.get('lat')
                    longitude = self.data_stream.TPV.get('lon')
                    altitude = self.data_stream.TPV.get('alt')
                    timestamp = self.data_stream.TPV.get('time')

                    if latitude is not None and longitude is not None:
                        self.sequence += 1
                        return {
                            "Sequence": self.sequence,
                            "Timestamp": timestamp,
                            "Latitude": latitude,
                            "Longitude": longitude,
                            "Altitude": altitude,
                        }
        except Exception as e:
            print(f"Error reading GPS data: {e}")
        return None
