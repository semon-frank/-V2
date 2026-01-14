import socket
import os
import sys
import struct

PORT = 5001

def send_file(sock, base_dir, file_path):
    rel_path = os.path.relpath(file_path, base_dir)
    rel_bytes = rel_path.encode("utf-8")

    sock.sendall(struct.pack("!I", len(rel_bytes)))
    sock.sendall(rel_bytes)

    size = os.path.getsize(file_path)
    sock.sendall(struct.pack("!Q", size))

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sock.sendall(chunk)

    print(f"[SENDER] Sent: {rel_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: sender.exe <receiver_ip> <file_or_dir>")
        return

    target_ip = sys.argv[1]
    src_path = sys.argv[2]

    base_dir = src_path if os.path.isdir(src_path) else os.path.dirname(src_path)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, PORT))

    if os.path.isfile(src_path):
        send_file(sock, base_dir, src_path)
    else:
        for root, _, files in os.walk(src_path):
            for name in files:
                send_file(sock, base_dir, os.path.join(root, name))

    sock.close()
    print("[SENDER] All files sent.")

if __name__ == "__main__":
    main()
