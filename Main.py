import sys
import random
from collections import deque

import pygame
import os
import math
from pygame.locals import *

SIZE = WIDTH, HEIGHT = 284 * 2, 512

FPS = 63
frame = 0

def load_image(img_file_name):
    file_name = os.path.join('.', 'Images', img_file_name)
    img = pygame.image.load(file_name)
    img.convert_alpha()
    return img




class Bird(pygame.sprite.Sprite):
    i = 0
    WIDTH = 32
    HEIGHT = 32
    SINK_SPEED = 4.5
    CLIMB_SPEED = 5
    CLIMB_DURATION = 1300

    def __init__(self):
        super(Bird, self).__init__()
        self.x = 50
        self.y = 256
        self.image = load_image('bird.png')
        self.state = 'down'
        self.flap_clock = pygame.time.Clock()
        self.flap_time_left = 0
        self.flap_start = None
        self.fall_start = pygame.time.get_ticks()
        self.fall_duration = None
        self.velocity = None

        self.mask = pygame.mask.from_surface(self.image)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def fly_down(self):
        self.fall_duration = pygame.time.get_ticks() - self.fall_start
        self.y += self.SINK_SPEED * (self.fall_duration/800+0.4)

    def fly_up(self):
        if self.flap_time_left <= 0.1:
            self.change_state('down')
        frac_climb_done = 1 - abs(self.flap_time_left/1000)
        self.flap_time_left = self.flap_time_left - (pygame.time.get_ticks() - self.flap_start)
        self.y -= self.CLIMB_SPEED * self.velocity
        self.velocity = 1 - frac_climb_done

    def update(self):
        if self.state == 'down':
            self.fly_down()
        else:
            self.fly_up()

    def change_state(self, state):
        if state == 'up':
            self.velocity = 1
            self.state = 'up'
            self.flap_time_left = self.CLIMB_DURATION
            self.flap_start = pygame.time.get_ticks()
            self.fly_up()

        else:
            self.fall_start=pygame.time.get_ticks()
            self.fly_down()
            self.state = 'down'


class PipeLine(pygame.sprite.Sprite):
    MINIMUM_GAP = 3*Bird.HEIGHT
    SPEED = 2
    START_POINT = (256*2) -1
    END_POINT = 0
    WIDTH = 80
    HEIGHT=512
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 150
    PIECIES_NUMBER = 16
    GAP_PIECES = 6
    def __init__(self):
        super(PipeLine, self).__init__()
        self.x = float(self.START_POINT)
        self.pipe_body_img = load_image('pipe_body.png')
        self.pipe_end_img = load_image('pipe_end.png')
        self.top_pieces = random.randint(1, 10)
        self.bot_pieces = self.PIECIES_NUMBER - self.top_pieces - self.GAP_PIECES
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT),SRCALPHA)
        self.image.convert()   # speeds up blitting
        self.image.fill((0, 0, 0, 0))

        for i in range(self.top_pieces):
            self.image.blit(self.pipe_body_img, (0, i * self.PIECE_HEIGHT))
        top_pipe_end_y = self.top_pieces * self.PIECE_HEIGHT
        self.image.blit(self.pipe_end_img, (0, top_pipe_end_y))

        for i in range(1, self.bot_pieces+1):
            self.image.blit(self.pipe_body_img, (0, self.HEIGHT - i * self.PIECE_HEIGHT))
        bottom_pipe_end_y = self.HEIGHT - self.PIECE_HEIGHT * self.bot_pieces
        bottom_end_piece_pos = (0, bottom_pipe_end_y - self.PIECE_HEIGHT)
        self.image.blit(self.pipe_end_img, bottom_end_piece_pos)

        self.mask = pygame.mask.from_surface(self.image)

    @property
    def rect(self):
        return pygame.Rect(self.x, 0, PipeLine.WIDTH, PipeLine.PIECE_HEIGHT)

    def update(self):
        self.x -= 2

    @property
    def is_visible(self):
        return -PipeLine.WIDTH < self.x < self.START_POINT

    def collides_with(self, bird):
        return pygame.sprite.collide_mask(self, bird)


is_game_over = False
def main():
    pygame.init()
    score = 0
    font = pygame.font.SysFont("terminal", 72)
    font2 = pygame.font.SysFont("terminal", 30)
    score_display = font.render("Your score: " + str(score), True, (0, 0, 0))
    def check_collision():
        if bird.y > 512 :
            game_over()
    def game_over():
        draw_background()

        text = font.render("GAME OVER", True, (255, 0, 0))
        game_display.blit(text,  (320 - text.get_width() // 2, 240 - text.get_height() // 2))
        game_display.blit(score_display, (300 - score_display.get_width() // 2, 150- score_display.get_height() // 2))
        pygame.display.flip()
        global is_game_over
        is_game_over = True
        while True:
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif Event.type == pygame.KEYUP and pygame.KEYUP:
                    pygame.quit()
                    quit()

    def draw_bird():

        if bird.state == 'up':
            bird_angle = bird.flap_time_left /1000 * 35
            rot_image = pygame.transform.rotate(bird.image, bird_angle)
            rot_rect = rot_image.get_rect(center=bird.rect.center)
            game_display.blit(rot_image, rot_rect)
        else:
            bird_angle = - bird.fall_duration / 1000 * 35
            rot_image = pygame.transform.rotate(bird.image, bird_angle)
            rot_rect = rot_image.get_rect(center=bird.rect.center)
            game_display.blit(rot_image, rot_rect)


    def draw_background():
        for x in (0, WIDTH / 2):
            game_display.blit(background, (x, 0))


    frame_clock = 0

    game_display = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    background = load_image('background.png')
    bird = Bird()
    pipes = deque()
    while not is_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYUP and pygame.KEYUP:
                if bird.state != 'up':
                    bird.change_state('up')

        bird.update()
        clock.tick(FPS)
        draw_background()
        draw_bird()

        for p in pipes:
            game_display.blit(p.image, p.rect)
            p.update()

        while pipes and not pipes[0].is_visible:
            pipes.popleft()

        if not frame_clock % PipeLine.ADD_INTERVAL:
            pipes.append(PipeLine())

        check_collision()
        if any(p.collides_with(bird) for p in pipes):
            game_over()



        frame_clock += 1
        score += 1
        score_display = font2.render("Your score: " + str(score), True, (0, 0, 0))
        game_display.blit(score_display, (100 - score_display.get_width() // 2, 500 - score_display.get_height() // 2))
        pygame.display.flip()

if __name__ == '__main__':
    main()