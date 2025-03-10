import asyncio
import websockets
import json
from auth import create_user, register_client, get_client, get_clients_by_user, get_coms_for_client, authenticate_user, authenticate_admin

# Dicionário para armazenar filas de mensagens por client_id
message_queues = {}

async def message_worker(client_id, websocket):
    """Worker que envia mensagens da fila para o client."""
    while True:
        if client_id in message_queues:
            queue = message_queues[client_id]
            if not queue.empty():
                message = await queue.get()
                try:
                    await websocket.send(json.dumps(message))
                except websockets.ConnectionClosed:
                    print(f"Connection closed for client {client_id}")
                    break
        await asyncio.sleep(1)  # Verifica a fila a cada segundo

async def handle_connection(websocket, path):
    try:
        # Recebe os dados de conexão
        data = await websocket.recv()
        data = json.loads(data)

        # Verifica o tipo de conexão
        connection_type = data.get('type')  # Pode ser 'admin', 'user' ou 'client'
        username = data.get('username')
        password = data.get('password')
        client_id = data.get('client_id')

        if connection_type == 'admin':
            # Conexão como admin
            if not authenticate_admin(username, password):
                await websocket.send(json.dumps({'status': 'error', 'message': 'Admin authentication failed'}))
                return

            await websocket.send(json.dumps({'status': 'success', 'message': 'Connected as admin'}))

            # Admin só pode criar usuários
            async for message in websocket:
                data = json.loads(message)
                action = data.get('action')

                if action == 'create_user':
                    new_username = data.get('username')
                    new_password = data.get('password')

                    success, message = create_user(username, password, new_username, new_password)
                    await websocket.send(json.dumps({'status': 'success' if success else 'error', 'message': message}))
                else:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid action for admin'}))

        elif connection_type == 'user':
            # Conexão como usuário
            if not authenticate_user(username, password):
                await websocket.send(json.dumps({'status': 'error', 'message': 'User authentication failed'}))
                return

            await websocket.send(json.dumps({'status': 'success', 'message': 'Connected as user'}))

            # Usuário só pode registrar clients
            async for message in websocket:
                data = json.loads(message)
                action = data.get('action')

                if action == 'register_client':
                    client_id = data.get('client_id')
                    coms = data.get('coms', [])
                    status = data.get('status', 'active')

                    success, message = register_client(username, password, username, client_id, coms, status)
                    await websocket.send(json.dumps({'status': 'success' if success else 'error', 'message': message}))
                else:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid action for user'}))

        elif connection_type == 'client':
            # Conexão como client
            if not authenticate_user(username, password):
                await websocket.send(json.dumps({'status': 'error', 'message': 'User authentication failed'}))
                return

            # Verifica se o client existe e pertence ao usuário
            client = get_client(client_id)
            if not client or client["user_id"] != username:
                await websocket.send(json.dumps({'status': 'error', 'message': 'Client not found or unauthorized'}))
                return

            await websocket.send(json.dumps({'status': 'success', 'message': 'Connected as client'}))

            # Cria uma fila para o client se não existir
            if client_id not in message_queues:
                message_queues[client_id] = asyncio.Queue()

            # Inicia o worker para enviar mensagens da fila para o client
            asyncio.create_task(message_worker(client_id, websocket))

            # Client só pode enviar mensagens
            async for message in websocket:
                data = json.loads(message)
                action = data.get('action')

                if action == 'send_message':
                    message_content = data.get('message')

                    # Obtém a lista de clients com os quais ele pode se comunicar
                    coms = get_coms_for_client(client_id)
                    if not coms:
                        await websocket.send(json.dumps({'status': 'error', 'message': 'No clients to communicate with'}))
                        continue

                    # Repassa a mensagem para os clients na lista de comunicação
                    for com_id in coms:
                        com_client = get_client(com_id)
                        if com_client:
                            # Cria uma fila para o client se não existir
                            if com_id not in message_queues:
                                message_queues[com_id] = asyncio.Queue()

                            # Adiciona a mensagem na fila do client
                            message = {
                                "status": "success",
                                "message": f"Message sent to {com_id}",
                                "from_client": client_id,
                                "to_client": com_id,
                                "content": message_content
                            }
                            await message_queues[com_id].put(message)
                        else:
                            await websocket.send(json.dumps({'status': 'error', 'message': f"Client {com_id} not found"}))
                else:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid action for client'}))

        else:
            await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid connection type'}))
            return

    except websockets.ConnectionClosed:
        print("Connection closed")

# Inicia o servidor WebSocket
start_server = websockets.serve(handle_connection, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()