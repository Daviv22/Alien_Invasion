class GameStats:
    """Acompanha as estatísticas da Invasão Alienígena."""

    def __init__(self, ai_game):
        """Inicializa as estatísticas"""
        self.settings = ai_game.settings
        self.reset_status()
        self.high_score = 0

    def reset_status(self):
        """Inicializa estatísticas que podem mudar durante o jogo"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1