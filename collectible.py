"""
@file collectible.py
@brief Collectible class for in-game items (e.g. carrots)
@author Your Name
@date 2024
"""

import pygame

class Collectible:
    """
    @brief Collectible item (e.g. carrot)
    """
    def __init__(self, x, y, width=20, height=20):
        """
        @brief Initialize collectible
        @param x int X coordinate
        @param y int Y coordinate
        @param width int Width of collectible
        @param height int Height of collectible
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def render(self, screen, camera):
        """
        @brief Render collectible (draw as an orange ellipse with green leaves)
        @param screen pygame.Surface Game window surface
        @param camera Camera Camera object
        """
        c_rect = camera.apply(self.rect)
        # Draw carrot body
        pygame.draw.ellipse(screen, (255, 140, 0), c_rect)
        # Draw carrot leaves
        leaf_x = c_rect.centerx
        leaf_y = c_rect.top
        pygame.draw.line(screen, (0, 200, 0), (leaf_x, leaf_y), (leaf_x, leaf_y-8), 3)
        pygame.draw.line(screen, (0, 180, 0), (leaf_x, leaf_y), (leaf_x-4, leaf_y-6), 2)
        pygame.draw.line(screen, (0, 180, 0), (leaf_x, leaf_y), (leaf_x+4, leaf_y-6), 2)
    
    def collect(self, player):
        """
        @brief Called when player collects this item
        @param player Player object
        """
        player.ammo += 5 