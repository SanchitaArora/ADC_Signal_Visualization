
import socket
import time
import os

FOLDER = "/Users/sanchitaarora/Documents/documents/socket_server/adc_files"
HOST = '127.0.0.1'
PORT = 12345

def list_files():
    return [f for f in os.listdir(FOLDER) if f.endswith('.txt')]

def main():
    files = list_files()
    print("Available files:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    idx = int(input("Select file number: ")) - 1
    filename = os.path.join(FOLDER, files[idx])
    interval = float(input("Enter time per sample in ms (e.g., 20): ")) / 1000.0

    with open(filename, 'r') as f:
        data = [line.strip().split(":")[-1] for line in f.readlines()]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Server listening on {HOST}:{PORT}...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    for value in data:
        conn.sendall(f"{value}\n".encode())
        time.sleep(interval)

    conn.close()
    print("Transmission finished.")

if __name__ == "__main__":
    main()

