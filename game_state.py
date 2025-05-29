"""
@file game_state.py
@brief Game state manager
@author Your Name
@date 2024
"""

from enum import Enum

class GameState(Enum):
    """
    @brief Game state enumeration
    """
    START_MENU = 1    # Start menu
    PLAYING = 2       # In game
    GAME_OVER = 3     # Game over
    LEVEL_COMPLETE = 4  # Level complete 