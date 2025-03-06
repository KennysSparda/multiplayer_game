import socket
import threading
import pickle

client_socket = None
game_state = {}
other_players = {}

def connect(ip, port):
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        # Inicia a thread pra receber dados do servidor
        threading.Thread(target=receive_data, daemon=True).start()
        return True
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return False

def receive_data():
    global game_state
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                game_state = pickle.loads(data)
        except:
            print('Conexão perdida com o servidor.')
            break
