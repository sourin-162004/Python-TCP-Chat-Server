import socket
import threading

HOST = '127.0.0.1' 
PORT = 5556 

# NEW: We changed this from a list [] to a dictionary {}
# It will look like this: {socket_object: "Username"}
clients = {} 

def broadcast(message, sender_socket):
    """Sends a message to all clients EXCEPT the one who sent it."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # If a client breaks, remove them
                client.close()
                if client in clients:
                    del clients[client]

def handle_client(client_socket, client_address):
    try:
        # NEW: The FIRST message received from a new connection is their username
        username = client_socket.recv(1024).decode('utf-8')
        
        # Add them to our dictionary
        clients[client_socket] = username
        
        print(f"\n[NEW CONNECTION] {username} ({client_address[0]}:{client_address[1]}) connected.")
        
        # Announce to everyone else that a new user joined
        join_message = f"--- {username} has joined the chat! ---"
        broadcast(join_message.encode('utf-8'), client_socket)
        
        # Now enter the normal chatting loop
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message or message.lower() == 'exit':
                break
                
            # Format the message with their custom username
            formatted_message = f"[{username}]: {message}"
            print(formatted_message) # Print to server console
            
            # Broadcast the message
            broadcast(formatted_message.encode('utf-8'), client_socket)
            
    except ConnectionResetError:
        pass # Handle forceful disconnects gracefully
            
    finally:
        # NEW: Clean up when they leave
        if client_socket in clients:
            username = clients[client_socket]
            print(f"\n[DISCONNECTED] {username} has left.")
            
            leave_message = f"--- {username} has left the chat. ---"
            broadcast(leave_message.encode('utf-8'), client_socket)
            
            del clients[client_socket] # Remove from dictionary
            
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[STARTING] Server is listening on {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE USERS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()