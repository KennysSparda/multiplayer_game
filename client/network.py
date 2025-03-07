# network.py
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
        threading.Thread(target=receive_data, daemon=True).start()
        return True
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return False

def receive_data():
    global game_state
    while True:
        try:
            data = b""
            while True:
                packet = client_socket.recv(4096)  # Buffer maior
                if not packet:
                    break
                data += packet
                if len(packet) < 4096:
                    break
            
            if data:
                game_state = pickle.loads(data)
        except Exception as e:
            print(f'Erro ao receber dados: {e}')
            break
