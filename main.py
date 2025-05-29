"""
@file main.py
@brief Main entry point of the game
@author Your Name
@date 2024
"""

import pygame
import sys
from game import Game

def main():
    """
    @brief Main game function
    """
    # Initialize Pygame
    pygame.init()
    
    # Set up game window
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Rabbit Adventure")
    
    # Create game instance
    game = Game(screen)
    
    # Main game loop
    while game.running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Render game
        game.render()
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        game.clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main() 