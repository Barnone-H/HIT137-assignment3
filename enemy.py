"""
@file enemy.py
@brief Enemy base class and specific enemy classes
@author Your Name
@date 2024
"""

import pygame
import math
from projectile import EnemyProjectile

class Enemy(pygame.sprite.Sprite):
    """
    @brief Enemy base class, inherits from pygame.sprite.Sprite
    """
    def __init__(self, x, y, health, speed, damage):
        """
        @brief Initialize enemy
        @param x int Initial x coordinate
        @param y int Initial y coordinate
        @param health int Health value
        @param speed float Movement speed
        @param damage int Damage value
        """
        super().__init__()
        # Create enemy image (temporarily using rectangle)
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))  # Blue color for enemy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Enemy properties
        self.health = health
        self.speed = speed
        self.damage = damage
        self.facing_right = True
        
    def take_damage(self, damage):
        """
        @brief Take damage
        @param damage int Damage value
        @return bool Whether dead
        """
        self.health -= damage
        return self.health <= 0
        
    def update(self, player):
        """
        @brief Update enemy state
        @param player Player Player object
        """
        pass
        
    def render(self, screen, camera):
        """
        @brief Render enemy
        @param screen pygame.Surface Game window surface
        @param camera Camera Camera object
        """
        # Draw body
        screen.blit(self.image, camera.apply(self))

class Grunt(Enemy):
    """
    @brief Basic enemy type
    """
    def __init__(self, x, y, patrol_left=None, patrol_right=None, platform_rect=None, health=50, damage=10):
        """
        @brief Initialize basic enemy
        @param x int Initial x coordinate
        @param y int Initial y coordinate
        @param patrol_left int Patrol left boundary
        @param patrol_right int Patrol right boundary
        @param platform_rect Rect Platform rectangle
        @param health int Health value
        @param damage int Damage value
        """
        super().__init__(x, y, health=health, speed=2, damage=damage)
        self.patrol_left = patrol_left if patrol_left is not None else x - 50
        self.patrol_right = patrol_right if patrol_right is not None else x + 50
        self.direction = 1  # 1: right, -1: left
        self.platform_rect = platform_rect
        self.shoot_cooldown = 0
        self.shoot_delay = 60
        
    def update(self, player):
        """
        @brief Update basic enemy state
        @param player Player Player object
        @return EnemyProjectile Return bullet object
        """
        # Patrol logic
        self.rect.x += self.speed * self.direction
        if self.rect.x < self.patrol_left:
            self.rect.x = self.patrol_left
            self.direction = 1
        elif self.rect.x > self.patrol_right:
            self.rect.x = self.patrol_right
            self.direction = -1
        self.facing_right = self.direction > 0
        # Shooting logic
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        # 只要玩家和敌人水平有重叠（比如距离小于100像素），就发射子弹
        on_same_platform = abs(player.rect.centerx - self.rect.centerx) < 100 and abs(player.rect.bottom - self.rect.bottom) < 80
        print(f"[DEBUG] Enemy update: player.rect={player.rect}, enemy.rect={self.rect}, on_same_platform={on_same_platform}")
        if on_same_platform and self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            proj = EnemyProjectile(self.rect.centerx, self.rect.centery, player.rect.centerx > self.rect.centerx)
            proj.image = pygame.Surface((32, 16))
            proj.image.fill((255,255,255))
            proj.rect = proj.image.get_rect(center=(self.rect.centerx, self.rect.centery))
            proj.damage = 15
            return proj
        return None

    def render(self, screen, camera):
        screen_pos = camera.apply(self)
        x, y = screen_pos.x, screen_pos.y
        # Draw body
        pygame.draw.rect(screen, (0, 0, 200), (x+8, y+16, 16, 24))
        # Draw head
        pygame.draw.ellipse(screen, (200, 200, 255), (x+8, y, 16, 16))
        # Draw left leg
        pygame.draw.line(screen, (0,0,0), (x+12, y+40), (x+12, y+56), 3)
        # Draw right leg
        pygame.draw.line(screen, (0,0,0), (x+20, y+40), (x+20, y+56), 3)
        # Draw left arm
        pygame.draw.line(screen, (0,0,0), (x+8, y+20), (x, y+32), 3)
        # Draw right arm
        pygame.draw.line(screen, (0,0,0), (x+24, y+20), (x+32, y+32), 3)
        # Draw eyes
        pygame.draw.ellipse(screen, (0,0,0), (x+12, y+6, 3, 3))
        pygame.draw.ellipse(screen, (0,0,0), (x+19, y+6, 3, 3))

class Gunner(Enemy):
    """
    @brief Gunner enemy type
    """
    def __init__(self, x, y, patrol_left=None, patrol_right=None, platform_rect=None, health=75, damage=5):
        """
        @brief Initialize gunner enemy
        @param x int Initial x coordinate
        @param y int Initial y coordinate
        @param patrol_left int Patrol left boundary
        @param patrol_right int Patrol right boundary
        @param platform_rect Rect Platform rectangle
        @param health int Health value
        @param damage int Damage value
        """
        super().__init__(x, y, health=health, speed=1.5, damage=damage)
        self.shoot_cooldown = 0
        self.shoot_delay = 60  # 1 second shooting interval
        self.patrol_left = patrol_left if patrol_left is not None else x - 80
        self.patrol_right = patrol_right if patrol_right is not None else x + 80
        self.direction = 1
        self.platform_rect = platform_rect
        
    def update(self, player):
        """
        @brief Update gunner state
        @param player Player Player object
        @return EnemyProjectile Return bullet object
        """
        # Patrol logic
        self.rect.x += self.speed * self.direction
        if self.rect.x < self.patrol_left:
            self.rect.x = self.patrol_left
            self.direction = 1
        elif self.rect.x > self.patrol_right:
            self.rect.x = self.patrol_right
            self.direction = -1
        self.facing_right = self.direction > 0
        # Shooting cooling
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        # 只要玩家和敌人水平有重叠（比如距离小于100像素），就发射子弹
        on_same_platform = abs(player.rect.centerx - self.rect.centerx) < 100 and abs(player.rect.bottom - self.rect.bottom) < 80
        print(f"[DEBUG] Enemy update: player.rect={player.rect}, enemy.rect={self.rect}, on_same_platform={on_same_platform}")
        if on_same_platform and self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            proj = EnemyProjectile(self.rect.centerx, self.rect.centery, player.rect.centerx > self.rect.centerx)
            proj.image = pygame.Surface((32, 16))
            proj.image.fill((255,255,255))
            proj.rect = proj.image.get_rect(center=(self.rect.centerx, self.rect.centery))
            proj.damage = 15
            return proj
        return None

    def render(self, screen, camera):
        screen_pos = camera.apply(self)
        x, y = screen_pos.x, screen_pos.y
        # Draw body (light blue)
        pygame.draw.rect(screen, (0, 100, 200), (x+8, y+16, 16, 24))
        # Draw head
        pygame.draw.ellipse(screen, (180, 220, 255), (x+8, y, 16, 16))
        # Draw left leg
        pygame.draw.line(screen, (0,0,0), (x+12, y+40), (x+12, y+56), 3)
        # Draw right leg
        pygame.draw.line(screen, (0,0,0), (x+20, y+40), (x+20, y+56), 3)
        # Draw left arm (gunner holds a gun)
        pygame.draw.line(screen, (0,0,0), (x+8, y+20), (x, y+32), 3)
        # Draw right arm (gun)
        pygame.draw.line(screen, (0,0,0), (x+24, y+20), (x+32, y+32), 3)
        pygame.draw.rect(screen, (80,80,80), (x+28, y+28, 8, 4))  # gun
        # Draw eyes
        pygame.draw.ellipse(screen, (0,0,0), (x+12, y+6, 3, 3))
        pygame.draw.ellipse(screen, (0,0,0), (x+19, y+6, 3, 3))

class Boss(Enemy):
    """
    @brief Boss enemy type
    """
    def __init__(self, x, y, platform_rect=None, health=250, damage=30):
        """
        @brief Initialize Boss
        @param x int Initial x coordinate
        @param y int Initial y coordinate
        @param platform_rect Rect Platform rectangle
        @param health int Health value
        @param damage int Damage value
        """
        super().__init__(x, y, health=health, speed=2, damage=damage)
        self.platform_rect = platform_rect
        self.shoot_cooldown = 0
        self.shoot_delay = 40
        
    def update(self, player):
        """
        @brief Update Boss state
        @param player Player Player object
        @return EnemyProjectile or None
        """
        # Boss moves within platform range
        if self.platform_rect:
            left = self.platform_rect.left
            right = self.platform_rect.right - 160
            if not hasattr(self, 'direction'):
                self.direction = 1
            self.rect.x += self.speed * self.direction
            if self.rect.x < left:
                self.rect.x = left
                self.direction = 1
            elif self.rect.x > right:
                self.rect.x = right
                self.direction = -1
        # Shoot green big bead
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        # 只要玩家和敌人水平有重叠（比如距离小于100像素），就发射子弹
        on_same_platform = abs(player.rect.centerx - self.rect.centerx) < 100 and abs(player.rect.bottom - self.rect.bottom) < 80
        print(f"[DEBUG] Enemy update: player.rect={player.rect}, enemy.rect={self.rect}, on_same_platform={on_same_platform}")
        if on_same_platform and self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            if self.facing_right:
                bx = self.rect.right + 36
            else:
                bx = self.rect.left - 80
            by = self.rect.centery + 40
            proj = EnemyProjectile(bx, by, self.facing_right)
            proj.image = pygame.Surface((32,32))
            proj.image.fill((0,255,0))  # Green big bullet
            proj.rect = proj.image.get_rect(center=(bx, by))
            proj.damage = 50
            return proj
        return None

    def render(self, screen, camera):
        screen_pos = camera.apply(self)
        x, y = screen_pos.x, screen_pos.y
        # Draw body (green, bigger)
        pygame.draw.rect(screen, (0, 200, 0), (x+20, y+32, 40, 32))
        # Draw head
        pygame.draw.ellipse(screen, (180, 255, 180), (x+20, y+8, 40, 24))
        # Draw left leg
        pygame.draw.line(screen, (0,100,0), (x+28, y+64), (x+28, y+80), 5)
        # Draw right leg
        pygame.draw.line(screen, (0,100,0), (x+52, y+64), (x+52, y+80), 5)
        # Draw left arm
        pygame.draw.line(screen, (0,100,0), (x+20, y+40), (x, y+56), 5)
        # Draw right arm
        pygame.draw.line(screen, (0,100,0), (x+60, y+40), (x+80, y+56), 5)
        # Draw eyes
        pygame.draw.ellipse(screen, (0,0,0), (x+32, y+18, 6, 6))
        pygame.draw.ellipse(screen, (0,0,0), (x+42, y+18, 6, 6)) 