class Settings:
    """Uma classe para guardar todas as configurações de Alien Invasion"""

    def __init__(self):
        """Inicializa as configurações do jogo"""

        # Configurações da tela
        self.screen_width = 1200
        self.scrren_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5

        # Configurações das balas
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3