import socket

class Client:
    def __init__(self):
        self.host = '10.255.77.139'  # Server IP
        self.port = 12345  # Server port
        self.client_socket = None

    def accept(self):
        """Connect to the server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print("Connected to the server.")

    def run_client(self, data):
        """Send data to the server."""
        if self.client_socket:
            self.client_socket.sendall(data)
            if data == b"CLOSE":
                print("Closing socket.")
                self.close()

    def close(self):
        """Close the client socket."""
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            print("Client socket closed.")
