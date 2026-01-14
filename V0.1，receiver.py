import socket
import os
import struct
import time

HOST = "0.0.0.0"
PORT = 5001
BASE_DIR = "RECEIVED_FILES"

def recv_all(sock, size):
    data = b""
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

def main():
    os.makedirs(BASE_DIR, exist_ok=True)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    print(f"[RECEIVER] Listening on {PORT} ...")

    conn, addr = s.accept()
    print(f"[RECEIVER] Connected from {addr}")

    while True:
        header = recv_all(conn, 4)
        if not header:
            break

        path_len = struct.unpack("!I", header)[0]
        rel_path = recv_all(conn, path_len).decode("utf-8")

        size_data = recv_all(conn, 8)
        file_size = struct.unpack("!Q", size_data)[0]

        target_path = os.path.join(BASE_DIR, rel_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "wb") as f:
            remaining = file_size
            while remaining > 0:
                chunk = conn.recv(min(4096, remaining))
                if not chunk:
                    break
                f.write(chunk)
                remaining -= len(chunk)

        print(f"[RECEIVER] Saved: {rel_path} ({file_size} bytes)")

    conn.close()
    s.close()

if __name__ == "__main__":
    main()
