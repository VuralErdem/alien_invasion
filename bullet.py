import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ships current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color


        #Erstellt ein Geschossrechteck bei (0, 0) und legt dann die richtige Position fest.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Speichert die Position des Geschosses als Fliesskommawert.
        self.y = float(self.rect.y)



    def update(self):
        """Move the bullet up the screen"""
        # Aktualisiert die Fliesskommaposition des Rechtecks
        self.y -= self.settings.bullet_speed
        # Aktualisiert die Position des Rechtecks.
        self.rect.y = self.y


    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
