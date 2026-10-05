import socket
import sys
import time
from datetime import datetime, timezone


def main():
    if len(sys.argv) != 3:
        print("Usage: python TCP-client.py <server-IP-address> <server-port-number>")
        return

    server_ip = sys.argv[1]

    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("[CLIENT] Server port must be an integer")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)

    try:
        print(f"[CLIENT] Connecting to {server_ip}:{server_port}")
        client_socket.connect((server_ip, server_port))

        request = "TIME"
        send_time = datetime.now(timezone.utc)
        rtt_start = time.perf_counter()
        print(f"[CLIENT] Sending request: {request}")
        print(f"[CLIENT] Request sent at: {send_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}")
        client_socket.sendall(request.encode())

        data = client_socket.recv(1024)
        rtt = (time.perf_counter() - rtt_start) * 1000
        receive_time = datetime.now(timezone.utc)

        if not data:
            print("[CLIENT] Server closed the connection without sending a response")
            return

        server_timestamp = data.decode()
        print(f"[CLIENT] Received timestamp: {server_timestamp}")

        client_time = receive_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        print(f"[CLIENT] Client time: {client_time}")
        print(f"[CLIENT] RTT: {rtt:.3f} ms")
        print(f"[CLIENT] Estimated client-to-server delay: {rtt / 2:.3f} ms")

        try:
            server_time = datetime.strptime(
                server_timestamp,
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc)
        except ValueError:
            print("[CLIENT] Server returned a timestamp in an unrecognized format")
            return

        clock_difference = (receive_time - server_time).total_seconds() * 1000
        print(
            f"[CLIENT] Difference between received server time "
            f"and client time: {clock_difference:.3f} ms"
        )

    except socket.timeout:
        print("[CLIENT] No response received within 5 seconds")
    except OSError as error:
        print(f"[CLIENT] Network error: {error}")
    finally:
        client_socket.close()
        print("[CLIENT] Socket closed")


if __name__ == "__main__":
    main()
