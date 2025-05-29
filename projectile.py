"""
@file projectile.py
@brief Projectile class for handling carrot projectiles
@author Your Name
@date 2024
"""

import pygame

class Projectile(pygame.sprite.Sprite):
    """
    @brief Carrot projectile class, inherits from pygame.sprite.Sprite
    """
    def __init__(self, x, y, facing_right):
        """
        @brief Initialize projectile
        @param x int Initial x coordinate
        @param y int Initial y coordinate
        @param facing_right bool Whether shooting right
        """
        super().__init__()
        # Create projectile image (temporarily using rectangle)
        self.image = pygame.Surface((20, 10))
        self.image.fill((255, 165, 0))  # Orange color for carrot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Projectile properties
        self.speed = 10
        self.damage = 10
        self.facing_right = facing_right
        
    def update(self):
        """
        @brief Update projectile position
        """
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
            
        # Destroy if projectile leaves screen
        if self.rect.right < 0 or self.rect.left > 3000:
            self.kill()
            
    def render(self, screen, camera):
        """
        @brief Render projectile
        @param screen pygame.Surface Game window surface
        @param camera Camera Camera object
        """
        screen.blit(self.image, camera.apply(self))

class EnemyProjectile(pygame.sprite.Sprite):
    """
    @brief Enemy projectile class, inherits from pygame.sprite.Sprite
    """
    def __init__(self, x, y, facing_right):
        """
        @brief Initialize enemy projectile
        @param x int Initial x coordinate
        @param y int Initial y coordinate
        @param facing_right bool Whether shooting right
        """
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((0, 255, 0))  # Green color for enemy projectile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 6  # Moderate speed for visibility
        self.damage = 10
        self.facing_right = facing_right
        self.just_spawned = True
        
    def update(self):
        """
        @brief Update enemy projectile position
        """
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        # 不在这里kill，由game.py统一管理
        if self.just_spawned:
            self.just_spawned = False
        print(f"[DEBUG] EnemyProjectile update: {self}, rect={self.rect}")
            
    def render(self, screen, camera):
        """
        @brief Render enemy projectile
        @param screen pygame.Surface Game window surface
        @param camera Camera Camera object
        """
        print(f"[DEBUG] EnemyProjectile render: {self}, rect={self.rect}")
        screen.blit(self.image, camera.apply(self)) 