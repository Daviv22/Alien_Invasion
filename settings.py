class Settings:
    """Uma classe para guardar todas as configurações de Alien Invasion"""

    def __init__(self):
        """Inicializa as configurações do jogo"""

        # Configurações da tela
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5

        # Configurações das balas
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Configurações dos aliens
        self.alien_speed = 1.0
        self.fleet_drop_speed = 50
        # fleet_direction = 1 representa direita; -1 representa esquerda
        self.fleet_direction = 1

        # Configurações da nave
        self.ship_speed = 1.5
        self.ship_limit = 3