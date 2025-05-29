"""
@file player.py
@brief Player class for controlling the rabbit hero
@author Your Name
@date 2024
"""

import pygame
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    """
    @brief Player class, inherits from pygame.sprite.Sprite
    """
    def __init__(self, x, y):
        """
        @brief Initialize player
        @param x int Initial x coordinate
        @param y int Initial y coordinate
        """
        super().__init__()
        
        # Load player sprite (temporarily using rectangle)
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))  # Red color for player
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0  # Initial horizontal speed
        self.vel_y = 0  # Initial vertical speed
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = (y == 440)
        self.facing_right = True
        self.health = 100
        self.lives = 3
        self.ammo = 20
        self.shoot_cooldown = 0
        self.invincible = False
        self.invincible_timer = 0
        
        # Shooting
        self.max_ammo = 20
        self.shoot_delay = 20  # Shooting cooldown (frames)
        
        # Invincibility
        self.invincible_duration = 60  # 1 second invincibility (60 frames)
        
        # Movement state
        self.moving_left = False
        self.moving_right = False
        
    def handle_event(self, event):
        """
        @brief Handle player input event
        @param event pygame.event.Event Game event
        @return Projectile or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_left = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_right = True
            elif event.key == pygame.K_SPACE:
                self.jump()
            elif event.key == pygame.K_j:
                return self.shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_left = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_right = False
        return None
        
    def update(self):
        """
        @brief Update player state
        """
        # Process horizontal movement
        if self.moving_left:
            self.rect.x -= self.speed
            self.facing_right = False
        if self.moving_right:
            self.rect.x += self.speed
            self.facing_right = True
            
        # Apply gravity (only when player is not on the ground)
        if not self.on_ground:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
        
        # Update shooting cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Update invincible time
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Reset on_ground every frame, set to True only after collision detection
        # self.on_ground = False
        
    def jump(self):
        """
        @brief Execute jump
        """
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            
    def shoot(self):
        """
        @brief Shoot carrot
        @return Projectile or None If successful, return bullet object; otherwise, return None
        """
        if self.ammo > 0 and self.shoot_cooldown == 0:
            self.ammo -= 1
            self.shoot_cooldown = self.shoot_delay
            return Projectile(
                self.rect.centerx,
                self.rect.centery,
                self.facing_right
            )
        return None
        
    def take_damage(self, damage):
        """
        @brief Take damage
        @param damage int Damage value
        """
        if not self.invincible:
            self.health -= damage
            if self.health <= 0:
                self.lives -= 1
                if self.lives > 0:
                    self.health = 100
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            
    def render(self, screen, camera):
        """
        @brief Render player
        @param screen pygame.Surface Game window surface
        @param camera Camera Camera object
        """
        screen_pos = camera.apply(self)
        x, y = screen_pos.x, screen_pos.y
        # Draw only if not invincible or flashing
        if not self.invincible or self.invincible_timer % 4 < 2:
            # Draw rabbit body (white ellipse)
            pygame.draw.ellipse(screen, (255, 255, 255), (x, y+10, 40, 50))
            # Draw rabbit left ear
            pygame.draw.ellipse(screen, (255, 255, 255), (x+5, y-15, 10, 30))
            # Draw rabbit right ear
            pygame.draw.ellipse(screen, (255, 255, 255), (x+25, y-15, 10, 30))
            # Draw nose (pink small circle)
            pygame.draw.ellipse(screen, (255, 192, 203), (x+17, y+45, 6, 6))
            # Draw left eye (black small circle)
            pygame.draw.ellipse(screen, (0, 0, 0), (x+12, y+30, 4, 4))
            # Draw right eye (black small circle)
            pygame.draw.ellipse(screen, (0, 0, 0), (x+24, y+30, 4, 4)) 