class GameStats:
    """Acompanha as estatísticas da Invasão Alienígena."""

    def __init__(self, ai_game):
        """Inicializa as estatísticas"""
        self.settings = ai_game.settings
        self.reset_status()

    def reset_status(self):
        """Inicializa estatísticas que podem mudar durante o jogo"""
        self.ships_left = self.settings.ship_limit