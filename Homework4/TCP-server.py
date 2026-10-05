import socket
import sys
from datetime import datetime, timezone


def main():
    # Check that the user entered a port number
    if len(sys.argv) != 2:
        print("Usage: python TCP-server.py <server-port-number>")
        return

    # Get the port number from the command line
    port = int(sys.argv[1])

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the server to the given port
        server_socket.bind(("", port))

        # Start listening for incoming connections
        server_socket.listen(5)

        print(f"[SERVER] Listening on port {port}...")

        while True:
            # Wait for a client to connect
            client_socket, client_address = server_socket.accept()

            print(f"[SERVER] Connection received from {client_address}")

            # Receive the client's request
            data = client_socket.recv(1024).decode()

            if data:
                print(f"[SERVER] Received: {data}")

                # Get the current UTC time
                current_time = datetime.now(timezone.utc)

                # Convert the time to a timestamp string
                timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

                print(f"[SERVER] Sending timestamp: {timestamp}")

                # Send the timestamp back to the client
                client_socket.sendall(timestamp.encode())

            # Close the connection with the client
            client_socket.close()
            print("[SERVER] Connection closed")

    except KeyboardInterrupt:
        print("\n[SERVER] Server shutting down...")

    finally:
        # Close the server socket
        server_socket.close()
        print("[SERVER] Socket closed")


if __name__ == "__main__":
    main()