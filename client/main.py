# main.py
from ursina import *
import pickle
import network
from player import Player
from ui import create_menu

# Dentro do seu código principal
app = Ursina(borderless=False)

# Variáveis globais
player = None
dragging = False
mouse_offset = Vec2(0, 0)

# Criando o chão
chao = Entity(model='plane', scale=(100, 1, 100), color=color.gray, collider='box', position=(0, -1, 0))  # Chão fixo

# Cria a UI de conexão
ui_elements = create_menu()
menu_ui = ui_elements['menu_ui']
ip_input = ui_elements['ip_input']
port_input = ui_elements['port_input']
connect_button = ui_elements['connect_button']

# Função pra conectar no servidor e criar o jogador
def handle_connect():
    global player
    ip = ip_input.text
    port = int(port_input.text)
    if network.connect(ip, port):
        player = Player(element='fire', network=network, position=(0, 0, 0))  # Passa network para Player
        menu_ui.enabled = False

connect_button.on_click = handle_connect

def update():
    global dragging, mouse_offset, player
    if player and network.client_socket:
        player_data = {
            'position': player.position, 
            'rotation_y': player.controller.rotation_y,
            'element': player.element
        }
        try:
            network.client_socket.sendall(pickle.dumps(player_data))
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")

        current_ids = set(network.game_state.get('players', {}).keys())
        existing_ids = set(network.other_players.keys())

        for pid, pdata in network.game_state.get('players', {}).items():
            if pid != network.client_socket.getsockname()[1]:  # Evita atualizar a si mesmo
                # Verifica se o servidor mandou uma posição válida antes de atualizar
                if pdata['position'] == Vec3(0, 0, 0):
                    continue  # Pula essa iteração se a posição for (0,0,0)
                if pid not in network.other_players:
                    network.other_players[pid] = Entity(model='cube', color=color.blue)

                # Aplica posição e rotação
                network.other_players[pid].animate_position(pdata['position'], duration=0.1, curve=curve.linear)

                network.other_players[pid].rotation_y = pdata['rotation_y']  # Aplica a rotação

        for pid in existing_ids - current_ids:
            network.other_players[pid].remove()
            del network.other_players[pid]


app.run()