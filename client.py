import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 5556

# NEW: Ask for the username BEFORE connecting
username = input("Choose your username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Could not connect to the server. Is it running?")
    sys.exit()

# NEW: Send the username to the server immediately after connecting
client_socket.send(username.encode('utf-8'))

print("\n--- Connected to the chat room! Type 'exit' to leave. ---\n")

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n{message}")
        except:
            print("\n[Disconnected from the server]")
            client_socket.close()
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input()
    
    if message.lower() == 'exit':
        client_socket.send(message.encode('utf-8'))
        break
        
    client_socket.send(message.encode('utf-8'))

client_socket.close()