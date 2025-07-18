import asyncio
import websockets
import json

from create_questions import CreateQuestions

class WebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.create_questions = CreateQuestions()

    async def handler(self, websocket):
        print(f"Cliente conectado: {websocket.remote_address}")
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if "type" in data:
                    if data["type"] == "start_creation":
                        asyncio.run_coroutine_threadsafe(
                            self.create_questions.create_questions(websocket_server=self, websocket=websocket), loop=asyncio.get_event_loop()
                        )
        except websockets.exceptions.ConnectionClosed:
            self.monitorar_tasks()
            print(f"Cliente desconectado: {websocket.remote_address}")
            
        finally:
            self.connected_clients.remove(websocket)

    async def broadcast(self, message):
        if self.connected_clients:
            await asyncio.gather(*(client.send(message) for client in self.connected_clients))

    async def send_to_sender(self, message, sender):
        self.monitorar_tasks()
        await sender.send(message)

    def monitorar_tasks(self):
            tasks = asyncio.all_tasks()
            print(f"🔍 {len(tasks)} tasks rodando:")
            for task in tasks:
                print(f"  - {task.get_name()}")

    async def start(self):
        print(f"Servidor WebSocket rodando em ws://{self.host}:{self.port}")
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()  # Mantém o servidor ativo