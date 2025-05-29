"""
@file level.py
@brief Level system for managing game levels
@author Your Name
@date 2024
"""

import pygame
import random
from enemy import Grunt, Gunner, Boss
from collectible import Collectible

class Level:
    """
    @brief Level class for managing game levels
    """
    def __init__(self, level_number):
        """
        @brief Initialize level
        @param level_number int Level number
        """
        self.level_number = level_number
        self.width = 3000  # Total level width
        self.height = 600  # Level height
        self.platforms = []
        self.enemies = []
        self.collectibles = []
        self.spawn_point = (100, 100)  # Player spawn point
        self.flag_rect = None  # End flag
        
        # Generate different level layouts based on level number
        self.generate_level()
        
    def generate_level(self):
        """
        @brief Generate level layout
        """
        # Generate ground
        ground_height = 500
        ground = pygame.Rect(0, ground_height, self.width, 100)
        self.platforms.append(ground)
        
        # Player spawn point on ground
        self.spawn_point = (100, ground_height - 60)
        
        # Generate different platform layouts based on level number
        if self.level_number == 1:
            self.generate_level_1()
        elif self.level_number == 2:
            self.generate_level_2()
        elif self.level_number == 3:
            self.generate_level_3()
            
    def generate_level_1(self):
        """
        @brief Generate level 1 layout
        """
        # Add platforms
        platforms = [
            pygame.Rect(300, 400, 200, 20),
            pygame.Rect(600, 350, 200, 20),
            pygame.Rect(900, 300, 200, 20),
            pygame.Rect(1200, 350, 200, 20),
            pygame.Rect(1500, 400, 200, 20),
            pygame.Rect(1800, 350, 200, 20),
            pygame.Rect(2100, 300, 200, 20),
            pygame.Rect(2400, 350, 200, 20),
            pygame.Rect(2700, 400, 200, 20)
        ]
        self.platforms.extend(platforms)
        
        # 每个平台只生成一个敌人，且platform_rect=platform
        enemies = []
        for i, platform in enumerate(platforms):
            enemy_x = platform.x + platform.width // 2
            enemy_y = platform.y - 60
            if i % 2 == 0:
                enemies.append(Grunt(enemy_x, enemy_y, platform_rect=platform))
            else:
                enemies.append(Gunner(enemy_x, enemy_y, platform_rect=platform))
            print(f"[DEBUG] Platform {i}: {platform}, Enemy: {enemies[-1].__class__.__name__}, Enemy rect: {enemies[-1].rect}")
        self.enemies.extend(enemies)
        
        # 玩家出生点设置在第一个平台表面
        self.spawn_point = (platforms[0].x + 10, platforms[0].y - 60)
        print(f"[DEBUG] Player spawn point: {self.spawn_point}, Platform 0: {platforms[0]}")
        
        # Add collectibles above platforms
        collectibles = []
        for platform in platforms:
            collectible_x = platform.x + platform.width // 2
            collectible_y = platform.y - 80
            collectibles.append(Collectible(collectible_x, collectible_y))
        self.collectibles.extend(collectibles)
        
        # Add end flag at the right edge of the last platform
        last_plat = platforms[-1]
        flag_width = 20
        flag_height = 60
        self.flag_rect = pygame.Rect(last_plat.right - flag_width, last_plat.y - flag_height, flag_width, flag_height)
        
    def generate_level_2(self):
        """
        @brief Generate level 2 layout
        """
        # Add platforms
        platforms = [
            pygame.Rect(350, 400, 180, 20),
            pygame.Rect(650, 350, 180, 20),
            pygame.Rect(950, 300, 180, 20),
            pygame.Rect(1250, 250, 180, 20),
            pygame.Rect(1550, 300, 180, 20),
            pygame.Rect(1850, 350, 180, 20),
            pygame.Rect(2150, 400, 180, 20),
            pygame.Rect(2450, 350, 180, 20),
            pygame.Rect(2750, 300, 180, 20)
        ]
        self.platforms.extend(platforms)
        
        # Add enemies on platform surfaces
        enemies = []
        for platform in platforms:
            enemy_x = platform.x + platform.width // 2
            enemy_y = platform.y - 60
            enemies.append(Gunner(enemy_x, enemy_y, platform_rect=platform))
        self.enemies.extend(enemies)
        
        # Add collectibles above platforms
        collectibles = []
        for platform in platforms:
            collectible_x = platform.x + platform.width // 2
            collectible_y = platform.y - 80  # Place collectible above platform
            collectibles.append(Collectible(collectible_x, collectible_y))
        self.collectibles.extend(collectibles)
        
        # Add end flag at the right edge of the last platform
        last_plat = platforms[-1]
        flag_width = 20
        flag_height = 60
        self.flag_rect = pygame.Rect(last_plat.right - flag_width, last_plat.y - flag_height, flag_width, flag_height)
        
    def generate_level_3(self):
        """
        @brief Generate level 3 layout
        """
        # Add platforms
        platforms = [
            pygame.Rect(350, 400, 120, 20),
            pygame.Rect(550, 350, 120, 20),
            pygame.Rect(750, 300, 120, 20),
            pygame.Rect(950, 250, 120, 20),
            pygame.Rect(1150, 200, 120, 20),
            pygame.Rect(1350, 250, 120, 20),
            pygame.Rect(1550, 300, 120, 20),
            pygame.Rect(1750, 350, 120, 20),
            pygame.Rect(1950, 300, 120, 20),
            pygame.Rect(2150, 250, 120, 20),
            pygame.Rect(2350, 200, 120, 20),
            pygame.Rect(2550, 250, 120, 20),
            pygame.Rect(2750, 300, 200, 20)
        ]
        self.platforms.extend(platforms)
        
        # Add enemies on platform surfaces
        enemies = []
        for idx, platform in enumerate(platforms):
            enemy_x = platform.x + platform.width // 2
            enemy_y = platform.y - 60
            if platform == platforms[-1]:
                enemies.append(Boss(enemy_x, enemy_y, platform_rect=platform))
            else:
                enemies.append(Gunner(enemy_x, enemy_y, platform_rect=platform))
        self.enemies.extend(enemies)
        
        # Add collectibles above platforms
        collectibles = []
        for platform in platforms:
            collectible_x = platform.x + platform.width // 2
            collectible_y = platform.y - 80  # Place collectible above platform
            collectibles.append(Collectible(collectible_x, collectible_y))
        self.collectibles.extend(collectibles)
        
        # Add end flag at the right edge of the last platform
        last_plat = platforms[-1]
        flag_width = 20
        flag_height = 60
        self.flag_rect = pygame.Rect(last_plat.right - flag_width, last_plat.y - flag_height, flag_width, flag_height)
        
    def check_collision(self, player):
        """
        @brief Check collision between player and level elements
        @param player Player Player object
        """
        # Reset on_ground every frame
        player.on_ground = False
        # Check platform collisions
        for platform in self.platforms:
            if player.rect.colliderect(platform):
                if player.vel_y > 0:  # Falling
                    player.rect.bottom = platform.top
                    player.vel_y = 0
                    player.jumping = False
                    player.on_ground = True  # Set on_ground when landing
                elif player.vel_y < 0:  # Jumping
                    player.rect.top = platform.bottom
                    player.vel_y = 0
        # Check collectible collisions
        for collectible in self.collectibles[:]:
            if player.rect.colliderect(collectible.rect):
                collectible.collect(player)
                self.collectibles.remove(collectible)
                
    def update(self, player):
        """
        @brief Update level state
        @param player Player Player object
        @return bool Whether boss is defeated
        """
        # Update enemies
        for enemy in self.enemies:
            enemy.update(player)
            
        # Check if boss is defeated
        if self.level_number == 3:
            for enemy in self.enemies:
                if isinstance(enemy, Boss) and enemy.health <= 0:
                    return True
        return False
        
    def render(self, screen, camera):
        """
        @brief Render level
        @param screen pygame.Surface Game window surface
        @param camera Camera Camera object
        """
        # Render platforms
        for platform in self.platforms:
            pygame.draw.rect(screen, (100, 100, 100), camera.apply(platform))
        # Render enemies
        for enemy in self.enemies:
            enemy.render(screen, camera)
        # Render collectibles
        for collectible in self.collectibles:
            collectible.render(screen, camera)
        # Render end flag (flagpole + flag)
        if self.flag_rect:
            flag = camera.apply(self.flag_rect)
            # Draw flagpole (white)
            pygame.draw.rect(screen, (255,255,255), flag)
            # Draw flag (red triangle)
            pygame.draw.polygon(screen, (255,0,0), [
                (flag.right, flag.top), (flag.right+20, flag.top+20), (flag.right, flag.top+40)
            ]) 