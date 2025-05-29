"""
@file camera.py
@brief Camera system for view following
@author Your Name
@date 2024
"""

import pygame

class Camera:
    """
    @brief Camera class for view following
    """
    def __init__(self, target):
        """
        @brief Initialize camera
        @param target Target to follow (usually player)
        """
        self.target = target
        self.offset_x = 0
        self.offset_y = 0
        self.smooth_factor = 0.1  # Smoothing factor, smaller value means smoother movement
        
    def update(self):
        """
        @brief Update camera position
        """
        # Calculate target position (center target on screen)
        target_x = self.target.rect.centerx - 400  # 400 is half of screen width
        target_y = self.target.rect.centery - 300  # 300 is half of screen height
        
        # Smoothly move camera
        self.offset_x += (target_x - self.offset_x) * self.smooth_factor
        self.offset_y += (target_y - self.offset_y) * self.smooth_factor
        
    def apply(self, entity):
        """
        @brief Apply camera offset to entity
        @param entity Game entity (can be Player object or pygame.Rect)
        @return pygame.Rect Entity with applied offset
        """
        if hasattr(entity, 'rect'):
            # If it's a Player object, use its rect attribute
            rect = entity.rect.copy()
        else:
            # If it's a pygame.Rect, use directly
            rect = entity.copy()
            
        return rect.move(-self.offset_x, -self.offset_y)
        
    def apply_point(self, point):
        """
        @brief Apply camera offset to point
        @param point tuple Point coordinates to apply offset
        @return tuple Point coordinates with applied offset
        """
        return (point[0] - self.offset_x, point[1] - self.offset_y) 