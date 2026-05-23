import asyncio
import websockets
import threading

connected_clients = set()

async def handle_client(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Standard peer-to-peer broadcast
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        connected_clients.remove(websocket)

# --- NEW: Admin Broadcast Logic ---
async def broadcast_admin_message(msg):
    """Sends a special admin message to all connected browsers."""
    # We add a secret tag so the webpage knows it's from the Admin
    admin_formatted = f"SERVER_ADMIN:{msg}" 
    
    for client in connected_clients:
        try:
            await client.send(admin_formatted)
        except:
            pass

def admin_input_thread(loop):
    """Runs in the background, waiting for you to type in the terminal."""
    while True:
        msg = input()
        if msg:
            # Safely push the message from this thread into the asyncio web loop
            asyncio.run_coroutine_threadsafe(broadcast_admin_message(msg), loop)
# -----------------------------------

async def main():
    # 1. Get the current async loop
    loop = asyncio.get_running_loop()
    
    # 2. Start our background thread to listen to your keyboard
    thread = threading.Thread(target=admin_input_thread, args=(loop,), daemon=True)
    thread.start()

    # 3. Start the web server
    async with websockets.serve(handle_client, "127.0.0.1", 5557):
        print("--- SERVER IS LIVE ---")
        print("Type a message here and press Enter to broadcast an Admin Announcement to all users!\n")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())