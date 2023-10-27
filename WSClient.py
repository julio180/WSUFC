import asyncio
import websockets

# PORT e ADDRESS devem vir de alguma váriavel de ambiente
PORT = "7890"
ADDRESS = "localhost"

class WSClient:
    def __init__(self):
        self.websocket = None

    async def conectar(self, uri):
        try:
            self.websocket = await websockets.connect(uri)
            print(f"Conectado a {uri}")
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    async def enviar(self, mensagem):
        if self.websocket:
            await self.websocket.send(mensagem)
            print(f"Enviado: {mensagem}")
        else:
            print("Não há conexão WebSocket ativa para enviar.")

    async def fechar(self):
        if self.websocket:
            await self.websocket.close()
            print("Conexão fechada.")
            self.websocket = None
        else:
            print("Não há conexão WebSocket ativa para fechar.")

# Exemplo de uso:
async def main():
    client = WSClient()
    await client.conectar("ws://" + ADDRESS + ":" + PORT)
    await client.enviar("Olá, servidor!")
    await client.fechar()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())





