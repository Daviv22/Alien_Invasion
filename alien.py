import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Uma classe para representar um único alien na frota"""

    def __init__(self, ai_game):
        """Inicializa o alien e define sua posição inicial"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carrega a imagem do alien e define atributos de retângulo
        self.image = pygame.image.load('projects/alien_invasion/images/alien.bmp')
        self.rect = self.image.get_rect()

        # Coloca cada novo alien próximo do topo esquerdo da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Guarda a posição horizontal exata do alien
        self.x = float(self.rect.x)

    def update(self):
        """Mova o alien para a direita ou para a esquerda"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Retorna True se o alien está na borda da tela"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)