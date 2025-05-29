"""
@file game.py
@brief 游戏核心类
@author Your Name
@date 2024
"""

import pygame
from player import Player
from level import Level
from camera import Camera
from game_state import GameState

class Game:
    """
    @brief 游戏核心类，管理游戏状态和主要逻辑
    """
    def __init__(self, screen):
        """
        @brief 初始化游戏
        @param screen pygame.Surface 游戏窗口表面
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.current_level = 1
        self.max_levels = 3
        
        # 游戏状态
        self.state = GameState.START_MENU
        self.game_over = False
        
        # 按钮
        self.start_button = pygame.Rect(300, 300, 200, 50)
        self.restart_button = pygame.Rect(300, 400, 200, 50)
        self.next_level_button = pygame.Rect(300, 400, 200, 50)
        self.victory_button = pygame.Rect(300, 400, 200, 50)
        
        # 初始化游戏组件
        self.reset_game()
        
    def reset_game(self):
        """
        @brief 重置游戏状态
        """
        self.score = 0
        self.current_level = 1
        self.game_over = False
        self.player = Player(100, 440)  # 440为地面顶部
        print(f"[DEBUG] Player rect after init: {self.player.rect}")
        self.camera = Camera(self.player)
        self.level = Level(self.current_level)
        # self.level.check_collision(self.player)  # 注释掉，避免出生点被推回地面
        self.projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        
    def handle_event(self, event):
        """
        @brief 处理游戏事件
        @param event pygame.event.Event 游戏事件
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.state == GameState.START_MENU:
                if self.start_button.collidepoint(mouse_pos):
                    self.state = GameState.PLAYING
                    
            elif self.state == GameState.GAME_OVER:
                if self.restart_button.collidepoint(mouse_pos):
                    self.reset_game()
                    self.state = GameState.PLAYING
                elif self.victory_button.collidepoint(mouse_pos):
                    self.state = GameState.START_MENU
                    self.reset_game()
                    
            elif self.state == GameState.LEVEL_COMPLETE:
                if self.next_level_button.collidepoint(mouse_pos):
                    self.current_level += 1
                    if self.current_level > self.max_levels:
                        self.state = GameState.START_MENU
                        self.reset_game()
                    else:
                        # 保留玩家状态
                        old_player = self.player
                        self.level = Level(self.current_level)
                        self.player = Player(self.level.spawn_point[0], self.level.spawn_point[1])
                        self.player.lives = old_player.lives
                        self.player.health = old_player.health
                        self.player.ammo = old_player.ammo
                        self.camera = Camera(self.player)
                        self.level.check_collision(self.player)
                        self.projectiles = pygame.sprite.Group()
                        self.enemy_projectiles = pygame.sprite.Group()
                        self.state = GameState.PLAYING
                        
            elif self.state == GameState.VICTORY:
                if self.victory_button.collidepoint(mouse_pos):
                    self.state = GameState.START_MENU
                    self.reset_game()
            
        if self.state == GameState.PLAYING:
            proj = self.player.handle_event(event)
            if proj:
                self.projectiles.add(proj)
            
    def update(self):
        """
        @brief 更新游戏状态
        """
        if self.state == GameState.PLAYING:
            print(f"[DEBUG] Game update frame, player rect: {self.player.rect}")
            self.player.update()
            self.level.check_collision(self.player)
            self.level.update(self.player)
            self.camera.update()
            # 每一帧都遍历所有敌人并调用update
            new_enemy_projectiles = []
            for enemy in self.level.enemies:
                print(f"[DEBUG] Calling update for enemy: {enemy}, rect: {enemy.rect}")
                result = enemy.update(self.player)
                if result is not None:
                    new_enemy_projectiles.append(result)
            for proj in new_enemy_projectiles:
                self.enemy_projectiles.add(proj)
            self.projectiles.update()
            self.enemy_projectiles.update()
            for proj in list(self.projectiles):
                if proj.rect.right < 0 or proj.rect.left > self.level.width:
                    self.projectiles.remove(proj)
            for eproj in list(self.enemy_projectiles):
                if eproj.rect.right < 0 or eproj.rect.left > self.level.width:
                    self.enemy_projectiles.remove(eproj)
            for enemy in self.level.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    self.player.take_damage(enemy.damage)
            for eproj in list(self.enemy_projectiles):
                if getattr(eproj, 'just_spawned', False):
                    continue
                if self.player.rect.colliderect(eproj.rect):
                    self.player.take_damage(getattr(eproj, 'damage', 10))
                    self.enemy_projectiles.remove(eproj)
            for proj in list(self.projectiles):
                for enemy in self.level.enemies[:]:
                    if enemy.rect.colliderect(proj.rect):
                        dead = enemy.take_damage(proj.damage)
                        self.projectiles.remove(proj)
                        if dead:
                            self.level.enemies.remove(enemy)
                        break
            if self.player.lives <= 0:
                self.state = GameState.GAME_OVER
            if self.current_level < self.max_levels:
                if self.player.rect.x >= self.level.width - 100:
                    self.state = GameState.LEVEL_COMPLETE
            else:
                if self.level.flag_rect and self.player.rect.colliderect(self.level.flag_rect):
                    self.state = GameState.VICTORY
            
    def render(self):
        """
        @brief 渲染游戏画面
        """
        # 清空屏幕
        self.screen.fill((0, 0, 0))
        
        if self.state == GameState.START_MENU:
            self.render_start_menu()
        elif self.state == GameState.PLAYING:
            self.render_game()
        elif self.state == GameState.GAME_OVER:
            self.render_game_over()
        elif self.state == GameState.LEVEL_COMPLETE:
            self.render_level_complete()
        elif self.state == GameState.VICTORY:
            self.render_victory()
            
    def render_start_menu(self):
        """
        @brief 渲染开始菜单
        """
        # 渲染游戏标题
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Pixel Rabbit Adventure", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(400, 150))
        self.screen.blit(title_text, title_rect)
        
        # 渲染开始按钮
        pygame.draw.rect(self.screen, (100, 200, 100), self.start_button)
        button_font = pygame.font.Font(None, 36)
        start_text = button_font.render("Start Game", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_rect)
        
        # 渲染操作说明
        controls_font = pygame.font.Font(None, 24)
        controls = [
            "Controls:",
            "Left/Right or A/D: Move",
            "Space: Jump",
            "J: Shoot",
            "R: Restart (when game over)"
        ]
        
        for i, text in enumerate(controls):
            control_text = controls_font.render(text, True, (200, 200, 200))
            self.screen.blit(control_text, (50, 400 + i * 30))
            
    def render_game(self):
        """
        @brief 渲染游戏画面
        """
        self.level.render(self.screen, self.camera)
        for proj in self.projectiles:
            proj.render(self.screen, self.camera)
        for eproj in self.enemy_projectiles:
            eproj.render(self.screen, self.camera)
        self.player.render(self.screen, self.camera)
        self.render_hud()
        
    def render_hud(self):
        """
        @brief 渲染HUD（抬头显示）
        """
        font = pygame.font.Font(None, 36)
        # 移除分数显示
        # score_text = font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        # self.screen.blit(score_text, (10, 10))
        health_text = font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 50))
        lives_text = font.render(f"Lives: {self.player.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 90))
        level_text = font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 130))
        ammo_text = font.render(f"Ammo: {self.player.ammo}", True, (255, 255, 255))
        self.screen.blit(ammo_text, (10, 170))
        
    def render_game_over(self):
        """
        @brief 渲染游戏结束画面
        """
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(400, 200))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(self.screen, (200, 100, 100), self.victory_button)
        button_font = pygame.font.Font(None, 36)
        restart_text = button_font.render("Back to Menu", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=self.victory_button.center)
        self.screen.blit(restart_text, restart_rect)
        
    def render_level_complete(self):
        """
        @brief 渲染关卡完成画面
        """
        font = pygame.font.Font(None, 72)
        complete_text = font.render("LEVEL COMPLETE!", True, (0, 255, 0))
        complete_rect = complete_text.get_rect(center=(400, 200))
        self.screen.blit(complete_text, complete_rect)
        pygame.draw.rect(self.screen, (100, 200, 100), self.next_level_button)
        button_font = pygame.font.Font(None, 36)
        if self.current_level < self.max_levels:
            next_text = button_font.render("Next Level", True, (255, 255, 255))
        else:
            next_text = button_font.render("Back to Menu", True, (255, 255, 255))
        next_rect = next_text.get_rect(center=self.next_level_button.center)
        self.screen.blit(next_text, next_rect)

    def render_victory(self):
        font = pygame.font.Font(None, 72)
        victory_text = font.render("You Are Win", True, (0, 255, 0))
        victory_rect = victory_text.get_rect(center=(400, 200))
        self.screen.blit(victory_text, victory_rect)
        pygame.draw.rect(self.screen, (100, 200, 100), self.victory_button)
        button_font = pygame.font.Font(None, 36)
        menu_text = button_font.render("Back to Menu", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=self.victory_button.center)
        self.screen.blit(menu_text, menu_rect) 