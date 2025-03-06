from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController

class Player(Entity):
    def __init__(self, element, **kwargs):
        super().__init__(model='cube', color=color.orange, **kwargs)
        self.element = element
        self.visible = False  # Torna o modelo invisível para o próprio jogador

        # Usando FirstPersonController para facilitar a movimentação
        self.controller = FirstPersonController()

    def update(self):
        # Atualizar a posição do jogador, mesmo com FirstPersonController
        # A movimentação do FirstPersonController já é tratada automaticamente
        if player:
            player_data = {'position': player.position, 'element': player.element}
            try:
                network.client_socket.sendall(pickle.dumps(player_data))  # Envia a posição para o servidor
            except Exception as e:
                print(f"Erro ao enviar dados: {e}")