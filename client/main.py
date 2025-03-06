from ursina import *
import pickle
import network
from player import Player
from ui import create_menu

app = Ursina(borderless=False)

# Variáveis globais
player = None
dragging = False
mouse_offset = Vec2(0, 0)

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
        player = Player(element='fire', position=(0, 0, 0))
        menu_ui.enabled = False

connect_button.on_click = handle_connect

def update():
    global dragging, mouse_offset, player
    if player and network.client_socket:
        player_data = {'position': player.position, 'element': player.element}
        try:
            network.client_socket.sendall(pickle.dumps(player_data))
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")

        for pid, pdata in network.game_state.get('players', {}).items():
            try:
                if pid != network.client_socket.getsockname()[1]:
                    if pid not in network.other_players:
                        network.other_players[pid] = Entity(model='cube', color=color.blue)
                    network.other_players[pid].position = pdata['position']
            except Exception as e:
                print(f"Erro ao atualizar jogador: {e}")

    if dragging:
        dx, dy = mouse.x - mouse_offset.x, mouse.y - mouse_offset.y
        window.position += Vec2(dx, dy)
        mouse_offset = Vec2(mouse.x, mouse.y)

def input(key):
    global dragging, mouse_offset
    if key == 'left mouse down' and mouse.position.y > 0.45:
        dragging = True
        mouse_offset = Vec2(mouse.x, mouse.y)
    elif key == 'left mouse up':
        dragging = False

app.run()
