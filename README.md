Project Title: Real-Time Web Chat Application using Asynchronous WebSockets
1. Project Objective
The objective of this project is to design and implement a full-stack, real-time chat application. It demonstrates the transition from traditional blocking TCP sockets to modern, asynchronous WebSocket protocols (ws://), allowing multiple browser-based clients to communicate simultaneously through a centralized Python server.
2. Technology Stack
   •	Backend (Server): Python 3.x
   •	Core Python Libraries: * websockets (for protocol upgrades and message framing)
       o	asyncio (for non-blocking, concurrent event loops)
   •	Frontend (Client): HTML5, CSS3, Vanilla JavaScript (Browser Native WebSocket API)
3. Key Features
   •	Asynchronous Concurrency: Utilizes Python's asyncio library to handle thousands of concurrent web connections on a           single thread without blocking I/O, replacing traditional multi-threading overhead.
   •	Dynamic User Identification: Clients are prompted for a custom username upon connecting via the web interface. The           frontend dynamically parses custom packet strings (e.g., Name|||Message) to update the UI and active user lists in           real-time.
   •	Peer-to-Peer Broadcasting: The server maintains a dynamic Set of active WebSocket connections. When a payload is             received, the server iterates through the set to broadcast the message to all other connected web peers.
   •	Server Admin Channel: Features specialized routing logic. The server can intercept messages containing the                   SERVER_ADMIN: header tag and route them to a dedicated, visually distinct announcement banner on all connected               frontends.
   •	Modern Web Interface: A fully styled, responsive frontend featuring CSS flexbox layouts, conditional message alignment       (left/right based on sender), and auto-scrolling chat boxes.
4. File Structure
   •	ws_server.py: The asynchronous backend hub. Binds to 127.0.0.1:5557, handles HTTP-to-WebSocket handshake upgrades,           manages the active client set, and routes messages.
   •	index.html: The frontend client interface. Contains the DOM elements, CSS styling, and JavaScript required to connect        to the server, capture user input, and manipulate the DOM upon receiving server broadcasts.
5. Execution Instructions
To test and run this architecture locally, follow these steps:
   1.	Start the Backend Server:
       o	Open your terminal or Command Prompt.
       o	Navigate to the project directory.
       o	Run the command: python ws_server.py
       o	Ensure you see the server listening on port 5557.
   2.	Connect the Clients:
       o	Open a modern web browser (Chrome, Edge, Firefox).
       o	Press Ctrl + O (or Cmd + O on Mac) and open the index.html file.
       o	Enter a username in the prompt.
       o	Open a new browser window, open index.html again, and enter a different username.
   3.	Testing Communication:
       o	Chat directly between the two browser windows.
       o	Notice the sidebar dynamically updating to reflect the active users.
6. Core Networking Concepts Demonstrated
   •	Protocol Upgrades: Transitioning a standard HTTP request into a persistent, full-duplex TCP tunnel via WebSocket             handshakes.
   •	Asynchronous Event Loops: Managing network state without standard Threading models.
   •	Custom Packet Formatting: Utilizing deliberate string delimiters (|||) to separate metadata (usernames) from actual          payload data (messages) across the application layer.
How to update this on GitHub:
Go to your GitHub repository page.
   1.	Click the pencil icon (Edit) in the top right corner of your current README.md file.
   2.	Delete the old text, paste this new text in, and click the green Commit changes button.

