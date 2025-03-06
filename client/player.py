from ursina import *

class Player(Entity):
    def __init__(self, element, **kwargs):
        super().__init__(model='cube', color=color.orange, **kwargs)
        self.element = element

    def update(self):
        self.position += self.forward * held_keys['w'] * time.dt
        self.position -= self.forward * held_keys['s'] * time.dt
        self.position -= self.right * held_keys['a'] * time.dt
        self.position += self.right * held_keys['d'] * time.dt
