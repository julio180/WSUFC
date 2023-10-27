import websockets
import asyncio

# PORT e ADDRESS devem vir de alguma váriavel de ambiente
PORT = 7890
ADDRESS = "localhost"

print("Server address -> " + ADDRESS + ":" + str(PORT))

connected = set()

async def handle(websocket, path):
    print("cliente conectado")
    connected.add(websocket)

    try:
        async for message in websocket:
            print("Menssagem recebida: " + message)
            for conn in connected:
                if conn != websocket:
                    await conn.send("said: " + message)
    #Verificar melhor forma de detectar conexão fechada
    except websockets.exceptions.ConnectionClosed as e:
        print("Cliente desconectado")
    finally:
        connected.remove(websocket)

async def main():
    async with websockets.serve(handle, ADDRESS, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())