# WSUFC

Um servidor simples de WebSocket em Python que permite a comunicação entre clientes autenticados.

## Requisitos

Certifique-se de ter o Python instalado na sua máquina. Este código foi desenvolvido e testado na versão 3.11.5, e é recomendável usar uma versão semelhante.

### Dependências

- `asyncio`: Módulo assíncrono para programação concorrente em Python.
- `websockets`: Biblioteca para implementação de WebSockets em Python.

Você pode instalar as dependências executando o seguinte comando no terminal:

```bash 
pip install asyncio websockets
```

## Como usar

1. Clone o repositório:

```bash 
git clone https://github.com/julio180/WSUFC.git
cd WSUFC
```

2. Execute o servidor:
```bash 
python WSServer.py
```

3. Conecte-se ao servidor WebSocket a partir de seus clientes, fornecendo o ID do cliente válido (presente no dicionário no código) para autenticação.

## Configurações

- `PORT`: Número da porta em que o servidor WebSocket será executado. Padrão: 7890.
- `ADDRESS`: Endereço do servidor. Padrão: "localhost".
- `DICTIONARY`: Lista de IDs de clientes válidos para autenticação.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou criar um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.