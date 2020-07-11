# 游戏环境

import os

import pygame
from ple.games import FlappyBird

class FlappyPaddle(FlappyBird):

    def _load_images(self):
        self.counter = 0        # 增加一个计数器
        self.last_score = 0     # 增加一个计分器
        # self._asset_dir = os.path.join('./', "assets")
        self._asset_dir = 'assets'
        # preload and convert all the images so its faster when we reset
        self.images["player"] = {}
        for c in ["red", "blue", "yellow"]:
            t = 'z' if c == 'red' or c == 'yellow' else 'b'
            image_assets = [
                os.path.join(self._asset_dir, f"{t}paddle.png"),
                os.path.join(self._asset_dir, f"{t}paddle1.png"),
                os.path.join(self._asset_dir, f"{t}paddle.png"),
            ]
            self.images["player"][c] = [pygame.image.load(
                im).convert_alpha() for im in image_assets]
        # background
        self.images["background"] = {}
        for b in ["day", "night"]:
            # path = os.path.join(self._asset_dir, "background-%s.png" % b)
            path = os.path.join(self._asset_dir, "ocean_s.jpg")

            self.images["background"][b] = pygame.image.load(path).convert()
        # pipes
        self.images["pipes"] = {}
        for c in ["red", "green"]:
            # path = os.path.join(self._asset_dir, "pipe-%s.png" % c)
            path = os.path.join(self._asset_dir, "shark_w_s.png")

            self.images["pipes"][c] = {}
            self.images["pipes"][c]["lower"] = pygame.image.load(
                path).convert_alpha()
            self.images["pipes"][c]["upper"] = pygame.transform.rotate(
                self.images["pipes"][c]["lower"], 180)

        path = os.path.join(self._asset_dir, "new_base.png")
        self.images["base"] = pygame.image.load(path).convert()

    def step(self, dt):
        self.game_tick += 1
        dt = dt / 1000.0

        self.score += self.rewards["tick"]

        # handle player movement
        self._handle_player_events()

        for p in self.pipe_group:
            hit = pygame.sprite.spritecollide(
                self.player, self.pipe_group, False)

            is_in_pipe = (p.x - p.width/2 - 20) <= self.player.pos_x < (p.x + p.width/2)
            for h in hit:  # do check to see if its within the gap.
                top_pipe_check = (
                    (self.player.pos_y - self.player.height/2 + 12) <= h.gap_start) and is_in_pipe
                bot_pipe_check = (
                    (self.player.pos_y +
                     self.player.height) > h.gap_start +
                    self.pipe_gap) and is_in_pipe

                if top_pipe_check:
                    self.lives -= 1

                if bot_pipe_check:
                    self.lives -= 1

            # is it past the player?
            if (p.x - p.width / 2) <= self.player.pos_x < (p.x - p.width / 2 + 4):
                self.score += self.rewards["positive"]

            # is out out of the screen?
            if p.x < -p.width:
                self._generatePipes(offset=self.width * 0.2, pipe=p)

        # fell on the ground
        if self.player.pos_y >= 0.79 * self.height - self.player.height:
            self.lives -= 1

        # went above the screen
        if self.player.pos_y <= 0:
            self.lives -= 1

        self.player.update(dt)
        self.pipe_group.update(dt)

        if self.lives <= 0:
            self.score += self.rewards["loss"]

        self.backdrop.draw_background(self.screen)
        self.pipe_group.draw(self.screen)
        self.backdrop.update_draw_base(self.screen, dt)
        # 绘制分数
        font_path = "assets/3D Isometric Bold.otf"
        # font_path = "assets/00pneumatix.woff.ttf"
        change_sizes = [40,55]
        if self.last_score != self.score:
            self.counter += 1
            self.last_score = self.score
        if self.counter > 1:
            self.counter = 0
        sz = change_sizes[self.counter]

        score_font = pygame.font.Font(font_path, sz)  # 创建一个font对象
        color = (255, 87, 0)  # 定义字体的颜色
        score_surface = score_font.render(str(int(self.score)), True, color)
        self.screen.blit(score_surface,(10,10))
        self.player.draw(self.screen)