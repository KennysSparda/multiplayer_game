from ursina import *

def create_menu():
    menu_ui = Entity(parent=camera.ui)
    
    Text("Endereço IP:", parent=menu_ui, position=(-0.2, 0.15))
    ip_input = InputField(default_value="127.0.0.1", parent=menu_ui, position=(0, 0.15))
    
    Text("Porta:", parent=menu_ui, position=(-0.2, 0))
    port_input = InputField(default_value="12345", parent=menu_ui, position=(0, 0))
    
    connect_button = Button(text="Conectar", parent=menu_ui, position=(0, -0.15), scale=(0.2, 0.1))
    
    return {
        'menu_ui': menu_ui,
        'ip_input': ip_input,
        'port_input': port_input,
        'connect_button': connect_button
    }
