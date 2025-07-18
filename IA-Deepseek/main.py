import asyncio
from websocket_server import WebSocketServer

# if __name__ == "__main__":
#     extractInfo = ExtractInfo(Path("Material de Referencia/Matrizes/matriz-de-referencia-de-matematica_2001.pdf"))
#     extractInfo.save_results(extractInfo.extract_text())



if __name__ == "__main__":
    try:
        server = WebSocketServer()
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\nServidor WebSocket encerrado.")
        
        
        