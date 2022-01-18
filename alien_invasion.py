import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        """For Full screen purposes"""
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #Bildet eine Instanz, um Spielstatistiken zu speichern und eine Anzeigetafel zu erstellen
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)


        # Erstellt eine Instanz zum Speichern der Spielstatistiken.


        self.ship = Ship(self)
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Erstellt die Play_Schaltfläche
        self.play_button = Button(self, "Play")
        


    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player click Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Setzt die Speileinstellungen zurück
            self.settings.initialize_dynamic_settings()

            #Setzt die Spielstatistiken zurück
            self.stats.reset_stats()

            #Blendet den Mauszeiger aus.
            pygame.mouse.set_visible(False)

        if self.play_button.rect.collidepoint(mouse_pos):
            #Setzt die Spielstatistik zurück
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()


            #Entfernt die verbliebenen Invasionsschiffe und Geschosse
            self.aliens.empty()
            self.bullets.empty()


            #Erstellt eine neue Flotte und zentriert das eigene Schiff
            self._create_fleet()
            self.ship.center_ship()


    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()



    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False



    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)



    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        #Aktualisiert die Geschosspositionen.
        self.bullets.update()

        # Entfernt die verschwundenen Geschosse.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Prüft, ob Geschosse ein Invasionsschiff getroffen haben.
        # Wenn ja, werden das Geschoss und das getroffene Schiff entfernt.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Zerstört vorhandene Geschosse und erstellt eine neue Flotte.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Setzt das Level herauf.
            self.stats.level += 1
            self.sb.prep_level()



    def _update_aliens(self):
        """ Check if the fleet is at an edge, then update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        #Prüft auf Kollisionen zwischen Invasoren und dem eigenen Schiff.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            

        #Prüft auf Invasoren, die den unteren Bildschirmrand erreichen.
        self._check_aliens_bottom()



    def _update_screen(self):
        """Update imgaes on the screen, and flip to the new screen"""

        # Zeichnet den Bildschirm bei jedem Schleifendurchlauf neu
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Zeichnet die Information über den Punktestand
        self.sb.show_score()

        #Zeichnet die Play-Schaltfläche nur bei inaktivem Spiel.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Macht den zuletzt gezeichneten Bidlschirm sichtbar.
        pygame.display.flip()



    def _create_fleet(self):
        """Create the fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Bestimmt die Anzahl der Reihen von Invasionschiffen, die auf den Bildschirm passen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Erstellt die Invasionsflotte
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)




    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """Respond appropriately if any alines have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #Verringert ships_left um 1 und aktualisiert die Anzeigetafel
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Entfernt alle verbliebenen Invasionsschiffe und Geschosse
            self.aliens.empty()
            self.bullets.empty()

            # Erstellt eine neue Flotte und zentriert das eigene Schiff
            self._create_fleet()
            self.ship.center_ship()

             # Hält das Spiel kurz an.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Gleiche Reaktion wie bei einer Kollision mit dem Schiff.
                self._ship_hit()
                break


if __name__ == "__main__":
    # Erstellt eine Spielinstanz und führ das Spiel aus.
    ai = AlienInvasion()
    ai.run_game()
