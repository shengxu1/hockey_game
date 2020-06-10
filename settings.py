
import pygame
from pygame.math import Vector2

canvas_width = 1500
canvas_height = 1000
fps = 40
leftwall = 100
rightwall = 1400
topwall = 100
bottomwall = 900

BLACK = (0, 0, 0)
BROWN = (165, 42, 42)
GREEN = (0, 200, 0)
LIGHTGREEN = (0, 255, 0)
RED = (200, 0, 0)
LIGHTRED = (255, 100, 100)

maxspeed = 8
rot_speed = 15 # must divide 45
xacc, yacc = 1, 1
player_size = (100, 80)
player_body_width = 26
player_body_height = 42
ball_player_offset = Vector2(-54, -27)

ball_radius = 5
ball_start_pos = (canvas_width / 2, 0)
ball_starting_angle = 90
stick_head_width, stick_head_height = 18, 24 # dimensions of rectangle of collision at head of stick
shot_speed = 25 # speed of ball when first shot out
ball_slowdown_interval = 4
ball_slowdown_rate = 1

wall_collision_factor = 1.2
min_wall_reflection_speed = 3

player_collision_y_factor = 10
player_collision_x_factor = 5

player1_color = "r"
player1_start_pos = (canvas_width / 2 + 200, canvas_height / 2)
player1_keyconfig = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_m)
player1_angle = 0

player2_color = "b"
player2_start_pos = (canvas_width / 2 - 200, canvas_height / 2)
player2_keyconfig = (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_v)
player2_angle = 180

goal_height = 250
goal_width = 100
goal_top = canvas_height / 2 - goal_height / 2

swing_angle = 45 # angle swung when shooting

# time to wait when goal scored 
goal_scored_countdown = fps * 1.5
max_speed_into_goal = 15

# cannot capture ball immediately after losing it
lost_ball_countdown = fps
