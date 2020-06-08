
import pygame
from pygame.math import Vector2

canvas_width = 980
canvas_height = 735
fps = 40

BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
LIGHTGREEN = (0, 255, 0)
RED = (200, 0, 0)
LIGHTRED = (255, 100, 100)

maxspeed = 10
rot_speed = 15 # must divide 45
xacc, yacc = 2, 2
player_size = (166, 134)
ball_player_offset = Vector2(-90, -45)

ball_radius = 8
ball_start_pos = (300, 300)
ball_start_speed = (0, -15)
stick_head_radius = ball_radius * 2 # area of collision circle at head of stick

player1_color = "r"
player1_start_pos = (500, 500)
player1_keyconfig = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_v)

swing_angle = 45 # angle swung when shooting