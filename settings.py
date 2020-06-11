
import pygame
from pygame.math import Vector2

fps = 40
game_duration = 90 # in seconds
fps_duration = game_duration * fps

canvas_width = 1200
canvas_height = 766
field_size = (canvas_width, canvas_height)
font_size = 45

leftwall = 48
rightwall = 1153
topwall = 197
bottomwall = 744

center_x = (leftwall + rightwall) // 2
center_y = (topwall + bottomwall) // 2

BLACK = (0, 0, 0)
BROWN = (165, 42, 42)
GREEN = (0, 200, 0)
LIGHTGREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
LIGHTRED = (255, 100, 100)

maxspeed = 8
rot_speed = 15 # must divide 45
xacc, yacc = 1, 1
player_size = (110, 88)
player_body_width = 30
player_body_height = 50
player_body_adjustment = 4
ball_player_offset = Vector2(-60, -30)

goal_height = 152
goal_width = leftwall
goal_size = (goal_width, goal_height)
goal_top = center_y - goal_height / 2

goalie_speed = 5
goalie_height = 42
goalie_width = 25
goalie_size = (goalie_width, goalie_height)
goalie_reflection_speed = 20

goalie_starty = goal_top + goal_height / 2
goalie1_startx = rightwall - goalie_width / 2
goalie2_startx = leftwall + goalie_width / 2
goalie1_keyconfig = pygame.K_UP, pygame.K_DOWN
goalie2_keyconfig = pygame.K_w, pygame.K_s

ball_radius = 5
ball_start_pos = (center_x, topwall)
ball_starting_angle = 90
stick_head_width, stick_head_height = 18, 24 # dimensions of rectangle of collision at head of stick
shot_speed = 20 # speed of ball when first shot out
ball_slowdown_interval = 4
ball_slowdown_rate = 1

wall_collision_factor = 1.2
min_wall_reflection_speed = 3

player_collision_y_factor = 10
player_collision_x_factor = 5

player1_start_pos = (center_x + 200, center_y)
player1_keyconfig = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_m)
player1_angle = 0

player2_start_pos = (center_x - 200, center_y)
player2_keyconfig = (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_v)
player2_angle = 180

swing_angle = 45 # angle swung when shooting

# time to wait when goal scored 
goal_scored_countdown = fps * 1.5
max_speed_into_goal = 15

# cannot capture ball immediately after losing it
lost_ball_countdown = fps / 2
