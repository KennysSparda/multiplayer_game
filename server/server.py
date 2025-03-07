# server.py
import socket
import threading
import pickle

HOST = '127.0.0.1'
PORT = 12345

game_state = {
    'players': {}
}

def handle_client(conn, addr):
    print(f'Conectado por {addr}')
    player_id = addr[1]
    game_state['players'][player_id] = {'position': (0, 0, 0), 'rotation_y': 0, 'element': None}

    try:
        while True:
            data = b""
            while True:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet
                if len(packet) < 4096:
                    break

            if not data:
                break
            player_data = pickle.loads(data)
            game_state['players'][player_id] = player_data  # Agora inclui posição e rotação

            conn.sendall(pickle.dumps(game_state))  # Retorna o estado atualizado para os clientes
    except:
        pass
    finally:
        print(f'Desconectado de {addr}')
        del game_state['players'][player_id]
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Servidor escutando em {HOST}:{PORT}')
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == '__main__':
    start_server()
