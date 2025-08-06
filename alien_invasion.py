import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvasion:
    """Classe geral para controlar os ativos e comportamento do jogo."""

    def __init__(self):
        """Inicializa o jogo, e cria os recursos do jogo"""
        pygame.init()

        self.clock = pygame.time.Clock()

        self.settings = Settings()

        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Cria uma instância para guardar estatísticas do jogo
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Começa Alien Invasion em um estado ativo
        self.game_active = False

        # Faz o botão de play
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Começa o loop principal do jogo"""
        while True:
            self._check_events()    # Espera por eventos do mouse e do teclado

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()   # Atualiza a tela
            self.clock.tick(60)

    def _check_events(self):
        """Responde a eventos de teclas e mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._chek_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    
    def _chek_keydown_events(self, event):
        """Responde a pressionamento teclas"""
        if event.key == pygame.K_RIGHT:
            # Mova a nav para a direita
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responde a levantamento das teclas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Cria uma nova bala e a adiciona ao grupo das balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_screen(self):
        """Atualiza imagens na tela, e muda para a nova tela"""

        # Redesenha a tela durante cada passagem pelo loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.update()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Desenha o botão de play se o jogo estiver inativo
        if not self.game_active:
            self.play_button.draw_button()
        
        # Faz a tela desenhada mais recentemente visível
        pygame.display.flip()

    def _update_bullets(self):
        """Atualiza a posição das balas e deleta as já disparadas"""
        # Atualiza posição de balas
        self.bullets.update()

        # Deletando balas que desapareceram
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Responde a colisão bala-alien"""
        # Remove qualquer bala e alien que se colidiram
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destrói balas existentes e cria uma nova frota
            self.bullets.empty()
            self._create_fleet()

    def _create_alien(self, x_position, y_position):
        """Cria um alien e coloca na fileira"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """Cria uma frota de aliens"""
        # Cria um alien e continua adicionando aliens até não haver mais espaço
        # Espaçamento entre aliens é a largura e altura de um alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Terminada uma fileira; reseta valor x, e incrementa valor y
            current_x = alien_width
            current_y += 2 * alien_height

    def _update_aliens(self):
        """Checa se a frota  está na borda, então atualiza as posições de todos os aliens na frota"""
        self._check_fleet_edges()
        self.aliens.update()

        # Checa colisões alien-nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Checa por aliens alcançando o fundo da tela
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        """Responde apropriadamente se qualquer alien bateu numa borda"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Muda a direção da frota"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Responde à nave ser atingida por um alien"""
        if self.stats.ships_left > 0:
            # Decrementa ships_left
            self.stats.ships_left -= 1

            # Se livra de qualquer balas e aliens sobrando
            self.bullets.empty()
            self.aliens.empty()

            # Cria uma nova frota e centraliza a nave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Checa se qualquer alien alcançou o fundo da tela"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Trata isso como se a nave fosse atingida
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Começa um novo jogo quando o jogador clica no Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reinicia as estatísticas do jogo
            self.stats.reset_status()
            self.game_active = True

            # Se livra de qualquer balas e aliens restantes
            self.bullets.empty()
            self.aliens.empty()

            # Cria uma nova frota e centraliza a nave
            self._create_fleet()
            self.ship.center_ship()

if __name__ == '__main__':
    """Fazer uma instância do jogo, e rodar o jogo"""
    ai = AlienInvasion()
    ai.run_game()
