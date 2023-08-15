from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from typing import List

app = FastAPI()

class ConnectionManager:
  def __init__(self):
    self.connections: List[WebSocket] = []

  async def connect(self, websocket: WebSocket):
    await websocket.accept()
    self.connections.append(websocket)

  # todo remove websocket from connections list on close
  async def disconnect(self, websocket: WebSocket):
    self.connections.remove(websocket)

  async def broadcast(self, data):
    for connection in self.connections:
      await connection.send_text(data)
  
  # async def whisper(self, data, recipient: int):
  #   for connection in self.connections:
  #     if connection[0] == recipient:
  #       await connection.send_text(data)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
  await manager.connect(websocket)
  try:
    while True:
      data = await websocket.receive_json()
      print(data)
      hex_data = bytes.fromhex(data["color"])
      await manager.broadcast(hex_data)
      # manager.whisper(bytes.fromhex(data))
      # client.send(data.encode())
      
  except WebSocketDisconnect:
    await manager.disconnect(websocket)
    # client.close()
  finally:
    await manager.disconnect(websocket)