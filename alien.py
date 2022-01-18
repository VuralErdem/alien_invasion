import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """Initialize the aline and set its starting postiion"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Lädt das Bild des Invasionschiffs und legt das rect-Attribut fest.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Platziert jedes neue INvasionsschiff oben links auf dem Bildschirm.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height


        # Speichert die genaue Position des Invasionsschiffs.
        self.x = float(self.rect.x)



    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        """Move the alien right or left"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
