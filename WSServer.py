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
    # Função para autenticar um cliente com base no client_id.
    # Adiciona o cliente à lista de clientes autenticados se o ID for válido.
    if client_id in DICTIONARY:
        authenticated_clients[client_id] = websocket
        return True
    else:
        return False

async def handle(websocket, path):
    try:
        client_id = await websocket.recv()
        # Tenta autenticar o cliente com o ID recebido.
        if await authenticate_client(websocket, client_id):
            print(f"Cliente {client_id} conectado")

            # Aguarda mensagens do cliente autenticado.
            async for message in websocket:
                print(f"Mensagem recebida do {client_id}: {message}")
                # Coloca a mensagem na fila para ser enviada para outros clientes.
                message_queue.put((client_id, message))
        else:
            # Se a autenticação falhar, envia uma mensagem de erro e fecha a conexão.
            await websocket.send("Bad Request: ID não existe no dicionário.")
            await websocket.close()
    except websockets.exceptions.ConnectionClosed:
        # Remove o cliente autenticado se a conexão for fechada.
        del authenticated_clients[client_id]
        print(f"Conexão fechada para {client_id}")

async def send_messages():
    # Loop que envia mensagens para clientes autenticados.
    while True:
        if not message_queue.empty():
            client_id, message = message_queue.get()
            # Envia a mensagem para todos os clientes autenticados, exceto o remetente original.
            for client in authenticated_clients.values():
                if client != authenticated_clients[client_id]:
                    await client.send(f"{client_id} disse: {message}")
        # Aguarda um curto período antes de verificar a fila novamente.
        await asyncio.sleep(0.1)

async def main():
    # Inicia o servidor WebSocket e a função para enviar mensagens.
    start_server = websockets.serve(handle, ADDRESS, PORT)
    await asyncio.gather(start_server, send_messages())

if __name__ == "__main__":
    # Executa o loop principal do asyncio.
    asyncio.run(main())