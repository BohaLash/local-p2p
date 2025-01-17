import socket
import struct

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5004

TTL = 2  # 2-hop restriction in network
BUFFER_SIZE = 1024


def listen_for_clients():
    """
    Listen for discovery messages from other clients and respond.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((MCAST_GRP, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("Listening for clients...")
        while True:
            message, address = sock.recvfrom(BUFFER_SIZE)
            print(f"Discovery request received from {address}: {message.decode()}")

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as reply_socket:
                reply_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                reply_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                reply_socket.bind(("", MCAST_PORT))
                reply_socket.sendto(b"hi", address)


def discover_clients():
    """
    Broadcast a discovery message to find other clients.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
        sock.settimeout(2)

        sock.sendto(b"hello", (MCAST_GRP, MCAST_PORT))

        try:
            print("Discovering clients...")
            while True:
                response, address = sock.recvfrom(BUFFER_SIZE)
                print(f"Discovered client at {address}: {response.decode()}")

        except socket.timeout:
            print("Discovery completed.")


if __name__ == "__main__":
    discover_clients()
    listen_for_clients()
