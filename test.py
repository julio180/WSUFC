import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Criar um novo usuário (autenticação do administrador embutida)
        await websocket.send(json.dumps({
            'action': 'create_user',
            'admin_username': 'admin',
            'admin_password': 'admin123',
            'username': 'user1',
            'password': 'senha1'
        }))
        response = await websocket.recv()
        print(response)

        # Registrar um client para o usuário (autenticação do usuário embutida)
        await websocket.send(json.dumps({
            'action': 'register_client',
            'username': 'user1',
            'password': 'senha1',
            'user_id': 'user1',
            'client_id': 'id1',
            'coms': ['id2', 'id3'],
            'status': 'active'  # Novo atributo
        }))
        response = await websocket.recv()
        print(response)

        await websocket.send(json.dumps({
            'action': 'register_client',
            'username': 'user1',
            'password': 'senha1',
            'user_id': 'user1',
            'client_id': 'id2',
            'coms': ['id1', 'id3'],
            'status': 'active'  # Novo atributo
        }))
        response = await websocket.recv()
        print(response)

        await websocket.send(json.dumps({
            'action': 'register_client',
            'username': 'user1',
            'password': 'senha1',
            'user_id': 'user1',
            'client_id': 'id3',
            'coms': ['id1'],
            'status': 'active'  # Novo atributo
        }))
        response = await websocket.recv()
        print(response)

        # Iniciar o worker para receber mensagens
        await websocket.send(json.dumps({
            'action': 'listen_messages',
            'client_id': 'id1'
        }))

         # Iniciar o worker para receber mensagens
        await websocket.send(json.dumps({
            'action': 'listen_messages',
            'client_id': 'id2'
        }))

         # Iniciar o worker para receber mensagens
        await websocket.send(json.dumps({
            'action': 'listen_messages',
            'client_id': 'id3'
        }))

        # Enviar uma mensagem
        await websocket.send(json.dumps({
            'action': 'send_message',
            'user_id': 'user1',
            'client_id': 'id1',
            'message': 'Hello World'
        }))

        # Receber mensagens da fila
        while True:
            response = await websocket.recv()
            print(response)

asyncio.get_event_loop().run_until_complete(test())