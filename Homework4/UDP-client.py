import socket
import sys
from datetime import datetime, timezone


def main():
    # Check that the user entered an IP address and port
    if len(sys.argv) != 3:
        print("Usage: python UDP-client.py <server-IP-address> <server-port-number>")
        return

    # Get the server IP address and port
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout in case the packet is lost
    client_socket.settimeout(5)

    try:
        # Create the request message
        request = "TIME"

        # Record the time before sending the request
        send_time = datetime.now(timezone.utc)

        print(f"[CLIENT] Sending request to {server_ip}:{server_port}")

        # Send the request to the server
        client_socket.sendto(
            request.encode(),
            (server_ip, server_port)
        )

        # Wait for the server's response
        data, server_address = client_socket.recvfrom(1024)

        # Record the time when the response is received
        receive_time = datetime.now(timezone.utc)

        # Convert the response to a string
        server_timestamp = data.decode()

        print(f"[CLIENT] Received timestamp: {server_timestamp}")
        print(f"[CLIENT] Response received from {server_address}")

        # Get the client's local time
        client_time = receive_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        print(f"[CLIENT] Client time: {client_time}")

        # Calculate the round-trip time
        rtt = (receive_time - send_time).total_seconds() * 1000

        # Estimate one-way delay as half of the RTT
        one_way_delay = rtt / 2

        print(f"[CLIENT] RTT: {rtt:.3f} ms")
        print(f"[CLIENT] Estimated client-to-server delay: {one_way_delay:.3f} ms")

        # Convert the server timestamp into a datetime object
        server_time = datetime.strptime(
            server_timestamp,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ).replace(tzinfo=timezone.utc)

        # Calculate the difference between server and client time
        clock_difference = (
            receive_time - server_time
        ).total_seconds() * 1000

        print(
            f"[CLIENT] Difference between received server time "
            f"and client time: {clock_difference:.3f} ms"
        )

    except socket.timeout:
        # Handle the case where no response is received
        print("[CLIENT] No response received within 5 seconds")
        print("[CLIENT] Possible packet loss or server unavailable")

    except OSError as error:
        # Handle other network errors
        print(f"[CLIENT] Network error: {error}")

    finally:
        # Close the client socket
        client_socket.close()
        print("[CLIENT] Socket closed")


if __name__ == "__main__":
    main()