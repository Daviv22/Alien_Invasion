import pygame

class Ship:
    """Uma classe para gerenciar a nave"""

    def __init__(self, ai_game):
        """Inicializa a nave e coloca na posição inicial"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Carrega a imagem da nave
        self.image = pygame.image.load('projects/alien_invasion/images/ship.bmp')
        self.rect = self.image.get_rect()

        # Coloca cada nova nave no centro inferior da tela
        self.rect.midbottom = self.screen_rect.midbottom

        # Guarda um float para a posição horizontal exata da nave
        self.x = float(self.rect.x)

        # Bandeira de movimento; Começa com uma nave que não está se movendo
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Atualiza a posição da nave baseada na bandeira de movimento"""
        # Atualiza o valor x da nave, não o rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Atualiza o objeto rect a partir de self.x
        self.rect.x = self.x

    def blitme(self):
        """Desenha a nave na posição atual"""
        self.screen.blit(self.image, self.rect)