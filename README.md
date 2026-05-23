Project Title: Multi-Threaded TCP Chat Server with Admin Broadcasting
1. Project Objective
The objective of this project is to design and implement a real-time, multi-client chat application using pure TCP socket programming in Python. It demonstrates the practical application of the Transport Layer (TCP) of the OSI model, showcasing reliable, connection-oriented data transmission, concurrent client handling, and peer-to-peer data broadcasting.
2. Technology Stack
   •	Language: Python 3.x
   •	Core Libraries: * socket (for raw TCP/IPv4 network communication)
          o	threading (for handling concurrent user connections and asynchronous I/O)
3. Key Features
   •	Multi-Client Concurrency: Utilizes Python's threading module to spawn dedicated background threads for every connected client. This ensures the server remains non-blocking and can handle multiple users simultaneously.
   •	Custom Usernames: Implements an application-layer handshake where the client transmits a chosen username immediately upon connecting, allowing dynamic user identification within the chat.
   •	Peer-to-Peer Broadcasting: The server maintains a dynamic dictionary of active client sockets. When a message is received from one node, the server iterates through the dictionary to broadcast the payload to all other connected peers.
   •	Graceful Disconnections: Includes try/except exception handling to catch ConnectionResetError. If a client forcefully closes their terminal, the server safely drops their socket and broadcasts a departure announcement without crashing.
   •	Server Admin Overrides: Features a dedicated administrative thread on the server side that listens to standard input (STDIN). The server administrator can broadcast global, high-priority announcements directly to all clients in real-time.
4. File Structure
   •	server.py: The central hub. Binds to 127.0.0.1:5555, listens for incoming TCP connections, manages the active client dictionary, and routes messages.
   •	client.py: The endpoint interface. Connects to the server, prompts the user for a username, and utilizes multithreading to simultaneously listen for incoming data and wait for user keyboard input.
5. Execution Instructions (Command Prompt)
To test and run this architecture locally, follow these exact steps using Windows Command Prompt:
    1.	Start the Server:
          o	Open Command Prompt and navigate to the project directory.
          o	Run the command: python server.py
          o	The server will indicate it is listening for connections.
    2.	Connect Client 1:
          o	Open a second Command Prompt window in the same directory.
          o	Run the command: python client.py
          o	Enter a username (e.g., "Alice") when prompted.
    3.	Connect Client 2:
          o	Open a third Command Prompt window in the same directory.
          o	Run the command: python client.py
          o	Enter a username (e.g., "Bob").
     4.	Testing Communication:
          o	Type a message in Client 1's terminal; it will instantly appear in Client 2's terminal.
          o	Go back to the Server Terminal, type a message, and press Enter to test the global Admin Broadcast feature.
6. Core Networking Concepts Demonstrated
     •	Binding & Listening: Securing an IP address and Port namespace for dedicated application traffic.
     •	Blocking vs. Non-Blocking I/O: Using threads to bypass the inherent blocking nature of socket.accept() and socket.recv().
     •	Application Layer Protocols: Designing a strict order of operations (e.g., the client must send a username string before it is allowed to enter the main chat loop).
