import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
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