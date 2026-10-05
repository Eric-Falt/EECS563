import socket
import sys
from datetime import datetime, timezone


def main():
    # Check that the user entered a port number
    if len(sys.argv) != 2:
        print("Usage: python UDP-server.py <server-port-number>")
        return

    # Get the port number from the command line
    port = int(sys.argv[1])

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Bind the server to the given port
        server_socket.bind(("", port))

        print(f"[SERVER] UDP server listening on port {port}...")

        while True:
            # Wait for a message from a client
            data, client_address = server_socket.recvfrom(1024)

            print(f"[SERVER] Received from {client_address}: {data.decode()}")

            # Get the current UTC time
            current_time = datetime.now(timezone.utc)

            # Convert the time to a timestamp string
            timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            print(f"[SERVER] Sending timestamp: {timestamp}")

            # Send the timestamp back to the client
            server_socket.sendto(
                timestamp.encode(),
                client_address
            )

    except KeyboardInterrupt:
        print("\n[SERVER] Server shutting down...")

    finally:
        # Close the server socket
        server_socket.close()
        print("[SERVER] Socket closed")


if __name__ == "__main__":
    main()