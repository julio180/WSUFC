import os
import json
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Credenciais do administrador
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Arquivos JSON para armazenar usuários e clients
USERS_FILE = "users.json"
CLIENTS_FILE = "clients.json"

def load_data(filename):
    """Carrega dados de um arquivo JSON."""
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {"users": []} if filename == USERS_FILE else {"clientes": []}

def save_data(data, filename):
    """Salva dados em um arquivo JSON."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

def authenticate_admin(username, password):
    """Verifica se as credenciais são do administrador."""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def create_user(admin_username, admin_password, new_username, new_password):
    """Cria um novo usuário após autenticar o administrador."""
    if not authenticate_admin(admin_username, admin_password):
        return False, "Admin authentication failed"

    users_data = load_data(USERS_FILE)
    for user in users_data["users"]:
        if user["username"] == new_username:
            return False, "User already exists"

    users_data["users"].append({"username": new_username, "password": new_password})
    save_data(users_data, USERS_FILE)
    return True, "User created"

def authenticate_user(username, password):
    """Autentica um usuário."""
    users_data = load_data(USERS_FILE)
    for user in users_data["users"]:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def register_client(username, password, user_id, client_id, coms, status="active"):
    """Registra um client após autenticar o usuário."""
    if not authenticate_user(username, password):
        return False, "User authentication failed"

    clients_data = load_data(CLIENTS_FILE)
    for client in clients_data["clientes"]:
        if client["client_id"] == client_id:
            return False, "Client already exists"

    clients_data["clientes"].append({
        "user_id": user_id,
        "client_id": client_id,
        "coms": coms,
        "status": status  # Novo atributo
    })
    save_data(clients_data, CLIENTS_FILE)
    return True, "Client registered"

def get_client(client_id):
    """Retorna um client pelo ID."""
    clients_data = load_data(CLIENTS_FILE)
    for client in clients_data["clientes"]:
        if client["client_id"] == client_id:
            return client
    return None

def get_clients_by_user(user_id):
    """Retorna todos os clients de um usuário."""
    clients_data = load_data(CLIENTS_FILE)
    return [client for client in clients_data["clientes"] if client["user_id"] == user_id]

def get_coms_for_client(client_id):
    """Retorna a lista de clients com os quais um client pode se comunicar."""
    client = get_client(client_id)
    if client:
        return client["coms"]
    return []