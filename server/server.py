# server.py
import socket
import threading
import pickle

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345        # Porta para escutar as conexões

# Estado inicial do jogo
game_state = {
    'players': {}
}

# Função para lidar com cada conexão de cliente
def handle_client(conn, addr):
    print(f'Conectado por {addr}')
    player_id = addr[1]  # Usando a porta do cliente como ID único
    game_state['players'][player_id] = {'position': (0, 0, 0), 'element': None}

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Atualiza o estado do jogador
            player_data = pickle.loads(data)
            game_state['players'][player_id] = player_data

            # Envia o estado atualizado do jogo para o cliente
            conn.sendall(pickle.dumps(game_state))
    except:
        pass
    finally:
        print(f'Desconectado de {addr}')
        del game_state['players'][player_id]
        conn.close()

# Inicializa o servidor
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
