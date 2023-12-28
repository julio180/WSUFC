import asyncio
import websockets
from queue import Queue

PORT = 7890
ADDRESS = "localhost"
DICTIONARY = ["codeplay", "jogo", "Lado A", "Lado B"]

client_id = "none"
authenticated_clients = {}
message_queue = Queue()

async def authenticate_client(websocket, client_id):
    # Se o client_id for válido, adiciona o cliente à lista de clientes autenticados
    if client_id in DICTIONARY:
        authenticated_clients[client_id] = websocket
        return True
    else:
        return False

async def handle(websocket, path):
    try:
        client_id = await websocket.recv()
        if await authenticate_client(websocket, client_id):
            print(f"Cliente {client_id} conectado")

            async for message in websocket:
                print(f"Mensagem recebida do {client_id}: {message}")
                message_queue.put((client_id, message))
        else:
            await websocket.send("Bad Request: ID não existe no dicionário.")
            await websocket.close()
    except websockets.exceptions.ConnectionClosed:
        del authenticated_clients[client_id]
        print(f"Conexão fechada para {client_id}")

async def send_messages():
    while True:
        if not message_queue.empty():
            client_id, message = message_queue.get()
            for client in authenticated_clients.values():
                if client != authenticated_clients[client_id]:
                    await client.send(f"{client_id} disse: {message}")
        await asyncio.sleep(0.1)

async def main():
    start_server = websockets.serve(handle, ADDRESS, PORT)
    await asyncio.gather(start_server, send_messages())

if __name__ == "__main__":
    asyncio.run(main())