# Lesson 03 — WebSockets

## What Are WebSockets?

WebSockets provide **full-duplex, real-time communication** between client and server — both can send messages at any time.

```
HTTP (Request-Response):
Client ──request──→ Server
Client ←─response── Server
(Connection closed)

WebSocket (Persistent):
Client ←──────────→ Server
(Connection stays open, both can send anytime)
```

---

## Basic WebSocket Endpoint

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the connection

    while True:
        # Wait for a message from the client
        data = await websocket.receive_text()

        # Send a message back
        await websocket.send_text(f"You said: {data}")
```

---

## WebSocket Methods

| Method | Purpose |
|--------|---------|
| `await ws.accept()` | Accept the connection |
| `await ws.receive_text()` | Receive text message |
| `await ws.receive_json()` | Receive JSON message |
| `await ws.receive_bytes()` | Receive binary data |
| `await ws.send_text(data)` | Send text message |
| `await ws.send_json(data)` | Send JSON message |
| `await ws.send_bytes(data)` | Send binary data |
| `await ws.close()` | Close the connection |

---

## Chat Room Example

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Send a message to ALL connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast(f"🟢 {username} joined the chat!")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"🔴 {username} left the chat")

# Simple HTML client for testing
@app.get("/chat")
async def chat_page():
    return HTMLResponse(\"\"\"
    <html>
    <body>
        <h1>Chat Room</h1>
        <input id="username" placeholder="Username" />
        <button onclick="connect()">Connect</button>
        <ul id="messages"></ul>
        <input id="messageText" placeholder="Message" />
        <button onclick="sendMessage()">Send</button>

        <script>
        let ws;
        function connect() {
            const name = document.getElementById('username').value;
            ws = new WebSocket(`ws://localhost:8000/ws/${name}`);
            ws.onmessage = (event) => {
                const li = document.createElement('li');
                li.textContent = event.data;
                document.getElementById('messages').appendChild(li);
            };
        }
        function sendMessage() {
            ws.send(document.getElementById('messageText').value);
            document.getElementById('messageText').value = '';
        }
        </script>
    </body>
    </html>
    \"\"\")
```

---

## Key Takeaways

1. **WebSockets = persistent, bidirectional** communication
2. **`@app.websocket("/ws")`** defines WebSocket endpoints
3. **`ConnectionManager`** pattern for managing multiple clients
4. **Handle `WebSocketDisconnect`** for clean disconnection
5. **Use for real-time apps** — chat, live updates, notifications

---

> **Next Lesson**: [Routers & App Structure →](../04-routers-app-structure/)
