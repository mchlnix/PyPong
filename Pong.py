#!/usr/bin/python3
from _socket import SOCK_STREAM
from math import copysign
from socket import socket, AF_INET

import pygame

from Mirror import Mirror
from Score import Score
from Speedup import Speedup

pygame.init()

FRAME_RATE = 60

COLOR_BG = (0xAA, 0xBB, 00)
COLOR_PLAYER = (0x49, 0x56, 0x00)

PIXEL = 20

PLAYER_HEIGHT = 5 * PIXEL
PLAYER_WIDTH = PIXEL

BALL_HEIGHT = PIXEL
BALL_WIDTH = PIXEL

WIN_W, WIN_H = 500, 500

BYTE_IDLE = b"\x02"
BYTE_UP = b"\x01"
BYTE_DOWN = b"\x00"
BYTE_NEW_CON = b"\x03"

RN_PORT = 12346
PLAY_PORT = 12345

SND_BING = pygame.mixer.Sound("bing.wav")
SND_SCORE = pygame.mixer.Sound("score.wav")
SND_SCORE_OPP = pygame.mixer.Sound("score_opponent.wav")

screen = pygame.display.set_mode((WIN_W, WIN_H))

clock = pygame.time.Clock()

x_player, y_player = 0, 0
x_online, y_online = WIN_W - PLAYER_WIDTH, 0

x_ball, y_ball = 12 * PIXEL, 12 * PIXEL

delta_x, delta_y = - PIXEL, - PIXEL

ticks = 0

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("192.168.2.112", PLAY_PORT))

sock.listen(1)
conn, addr = sock.accept()

delta_x *= -1

score = Score()

COLLISION_DIRECTIONS = [(1, -2), (1, -1), (2, 0), (1, 1), (1, 2)]


def score_left():
    score.score_left()
    pygame.mixer.Sound.play(SND_SCORE)
    reset()


def score_right():
    score.score_right()
    pygame.mixer.Sound.play(SND_SCORE_OPP)
    reset()


font = pygame.font.SysFont("couriernew", 72)


def draw_score(surface: pygame.Surface):
    text = font.render(score.get_score(), True, COLOR_PLAYER)

    x = (WIN_W - text.get_width()) // 2
    y = 20

    surface.blit(text, (x, y))


def reset():
    global x_ball, y_ball, move_timer, speed_up
    x_ball, y_ball = 12 * PIXEL, 12 * PIXEL
    speed_up = 1
    move_timer = 16


move_timer = 16

x_mod = -1
y_mod = -1

speed_up = 1

powerup1 = Speedup(12 * PIXEL, 10 * PIXEL)
mirror = Mirror(12 * PIXEL, 20 * PIXEL)

while True:
    to_send = BYTE_IDLE

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]:
        if y_player + PLAYER_HEIGHT < WIN_H:
            y_player += PIXEL
            to_send = BYTE_DOWN
    elif keys[pygame.K_UP]:
        if y_player > 0:
            y_player -= PIXEL
            to_send = BYTE_UP

    # sock.send(to_send)

    # data = sock.recv(1)

    data = BYTE_UP

    if data == BYTE_UP:
        y_online -= PIXEL
    elif data == BYTE_DOWN:
        y_online += PIXEL

    if ticks % (move_timer / x_mod / speed_up) == 0:
        # player collision
        if x_player + BALL_WIDTH == x_ball and y_player <= y_ball < y_player + PLAYER_HEIGHT:
            ball_offset = (y_ball - y_player) // PIXEL

            x_mod, y_mod = COLLISION_DIRECTIONS[ball_offset]

            delta_x = int(copysign(1, x_mod) * PIXEL)
            delta_y = int(copysign(1, y_mod) * PIXEL)

            pygame.mixer.Sound.play(SND_BING)

        # online collision
        if (x_online - BALL_WIDTH) == x_ball and y_online <= y_ball < (y_online + PLAYER_HEIGHT):
            ball_offset = (y_ball - y_online) // PIXEL

            x_mod, y_mod = COLLISION_DIRECTIONS[ball_offset]

            delta_x = int(copysign(1, x_mod) * PIXEL)
            delta_y = int(copysign(1, y_mod) * PIXEL)

            delta_x *= -1

            pygame.mixer.Sound.play(SND_BING)

        if x_ball == 0:
            score_right()
        elif x_ball == WIN_W - BALL_WIDTH:
            score_left()

        x_ball += delta_x

        if powerup1.collides_with(x_ball, y_ball):
            speed_up = 2

        if mirror.collides_with(x_ball, y_ball):
            delta_x *= -1

    if y_mod != 0 and (ticks % (move_timer / y_mod / speed_up)) == 0:
        # screen collision

        if y_ball == 0:
            delta_y *= -1

        if y_ball + BALL_HEIGHT == WIN_H:
            delta_y *= -1

        y_ball += delta_y

        if powerup1.collides_with(x_ball, y_ball):
            speed_up = 2

        if mirror.collides_with(x_ball, y_ball):
            delta_x *= -1

    pygame.draw.rect(screen, COLOR_BG, (0, 0, WIN_W, WIN_H))

    # draw ourself

    pygame.draw.rect(screen, COLOR_PLAYER, (x_player, y_player, PLAYER_WIDTH, PLAYER_HEIGHT))

    # draw online

    pygame.draw.rect(screen, COLOR_PLAYER, (x_online, y_online, PLAYER_WIDTH, PLAYER_HEIGHT))

    # draw power up

    powerup1.draw(screen, COLOR_PLAYER)
    mirror.draw(screen, COLOR_PLAYER)

    # draw ball

    pygame.draw.rect(screen, COLOR_PLAYER, (x_ball, y_ball, BALL_WIDTH, BALL_HEIGHT))

    # draw the score

    draw_score(screen)

    pygame.display.update()

    clock.tick(FRAME_RATE)

    ticks += 1
