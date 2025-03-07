# player.py
from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController
import pickle
from time import time

class Player(Entity):
    def __init__(self, element, network, **kwargs):
        super().__init__(model='cube', color=color.orange, **kwargs)
        self.element = element
        self.visible = False
        self.network = network
        self.controller = FirstPersonController()
        self.last_sent_time = time()

    def update(self):
        now = time()
        if now - self.last_sent_time < 0.05:  # Envia dados a cada 0.05s (20 vezes por segundo)
            return
        self.last_sent_time = now

        player_data = {
            'position': self.controller.position, 
            'rotation_y': self.controller.rotation_y,
            'element': self.element
        }
        try:
            self.network.client_socket.sendall(pickle.dumps(player_data))
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")
