
import pygame
from pygame.math import Vector2

canvas_width = 980
canvas_height = 735
fps = 60

BLACK = (0, 0, 0)

maxspeed = 10
rot_speed = 9 # must divide 45
xacc, yacc = 2, 2
player_size = (166, 134)
ball_player_offset = Vector2(-90, -48)

ball_radius = 8
ball_start_pos = (300, 300)
ball_start_speed = (0, -15)

player1_color = "r"
player1_start_pos = (500, 500)