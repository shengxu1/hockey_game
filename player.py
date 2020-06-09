
import pygame
import settings
import util
import math

from util import Rect
from enum import Enum 

class Direction(Enum):
  STATIONARY = 0
  CLOCKWISE = 1
  COUNTERCLOCKWISE = 2

class State(Enum):
  NORMAL = 0
  SWINGING = 1

class Player(object):
  # key_config: (left, right, up, down, shoot)
  def __init__(self, color, key_config, start_pos, start_angle):
    self.orig_img = pygame.transform.scale(pygame.image.load(
      'images/%s-1.png' % color).convert_alpha(), settings.player_size)
    self.img = self.orig_img

    self.xspeed, self.yspeed = 0, 0
    self.pos = start_pos

    self.angle = self.target_angle = self.shoot_angle = start_angle
    self.direction = Direction.STATIONARY

    self.stick_head_radius = settings.ball_radius * 2

    self.left_key, self.right_key, self.up_key, self.down_key, self.shoot_key = key_config

    self.state = State.NORMAL

  def reinit(self, start_pos, start_angle):
    self.state = State.NORMAL
    self.xspeed, self.yspeed = 0, 0
    self.pos = start_pos
    self.angle = self.target_angle = self.shoot_angle = start_angle
    self.direction = Direction.STATIONARY
    self.img = self.orig_img

  def is_swinging(self):
    return self.state == State.SWINGING

  # just finished swinging
  def finished_swinging(self):
    return self.state == State.SWINGING and self.angle == self.target_angle == self.shoot_angle

  def get_speed(self):
    return math.sqrt(self.xspeed ** 2 + self.yspeed ** 2)

  def get_shot_velocity(self):
    base_x = - settings.shot_speed * math.cos(math.radians(self.angle))
    base_y = settings.shot_speed * math.sin(math.radians(self.angle))
    shot_x = base_x + self.xspeed
    shot_y = base_y + self.yspeed
    shot_speed = math.sqrt(shot_x ** 2 + shot_y ** 2)

    angle = math.degrees(math.atan(abs(shot_y/shot_x)))
    shot_angle = util.get_angle_from_quadrant(angle, shot_x, shot_y)

    return shot_speed, shot_angle

  def shoot(self):
    if self.state != State.SWINGING:
      # enter swinging state, note that speed and pos are kept the same
      self.state = State.SWINGING
      self.adjust_target_angle(util.mod_angle(self.angle - settings.swing_angle))
      self.shoot_angle = self.angle # angle before swinging is angle to shoot the ball
      assert(self.direction == Direction.CLOCKWISE)

  def rotate_angle(self):

    if self.direction == Direction.CLOCKWISE:
      self.angle = util.mod_angle(self.angle - settings.rot_speed)

    elif self.direction == Direction.COUNTERCLOCKWISE:
      self.angle = util.mod_angle(self.angle + settings.rot_speed)

  def target_angle_reached(self):
    if self.state == State.NORMAL:
      self.direction = Direction.STATIONARY
    else:
      if self.direction == Direction.CLOCKWISE: # just swung the stick to full potential
        self.adjust_target_angle(util.mod_angle(self.angle + settings.swing_angle))
      else: # in the middle of swinging
        assert(self.direction == Direction.COUNTERCLOCKWISE and self.state == State.SWINGING)
        self.direction = Direction.STATIONARY
        self.state = State.NORMAL

  def rotate(self):
    if self.angle == self.target_angle: 
      self.target_angle_reached()

    if self.direction == Direction.STATIONARY: return

    self.rotate_angle()
    self.img = pygame.transform.rotate(self.orig_img, self.angle)

  def get_direction(self, clockwise_angle, counterclockwise_angle):
    if clockwise_angle == 0 or counterclockwise_angle == 0:
      return Direction.STATIONARY

    assert(clockwise_angle + counterclockwise_angle == 360)  

    if clockwise_angle < counterclockwise_angle: return Direction.CLOCKWISE
    if counterclockwise_angle < clockwise_angle: return Direction.COUNTERCLOCKWISE

    # special case when clockwise and counterclockwise angles are equal
    if self.angle < 180:
      assert(self.target_angle == self.angle + 180)
      return Direction.COUNTERCLOCKWISE
    else:
      assert(self.target_angle == self.angle - 180)
      return Direction.CLOCKWISE     

  def adjust_target_angle(self, angle):
    self.target_angle = angle

    clockwise_angle = util.mod_angle(self.angle - self.target_angle)
    counterclockwise_angle = util.mod_angle(self.target_angle - self.angle)

    self.direction = self.get_direction(clockwise_angle, counterclockwise_angle)

  def accelerate_left(self):  
    self.xspeed = max(self.xspeed - settings.xacc, - settings.maxspeed)

  def accelerate_right(self):  
    self.xspeed = min(self.xspeed + settings.xacc, settings.maxspeed)

  def accelerate_up(self):   
    self.yspeed = max(self.yspeed - settings.yacc, - settings.maxspeed)
  
  def accelerate_down(self):   
    self.yspeed = min(self.yspeed + settings.yacc, settings.maxspeed)

  def slow_down(self):
    self.xspeed = util.slow_down(self.xspeed, settings.xacc)
    self.yspeed = util.slow_down(self.yspeed, settings.yacc)

  def move(self):
    self.pos = (self.pos[0] + self.xspeed, self.pos[1] + self.yspeed)

    # TODO: when close to goal, adjust angle

  def get_ball_pos(self):
    offset_rotated = settings.ball_player_offset.rotate(-self.angle)
    return self.pos[0] + offset_rotated[0], self.pos[1] + offset_rotated[1]

  def get_stick_head(self):
    stick_ball_offset = pygame.Vector2(settings.ball_radius, 0)
    offset_rotated = stick_ball_offset.rotate(-self.angle)

    ball_pos = self.get_ball_pos()
    return Rect(ball_pos[0] + offset_rotated[0], ball_pos[1] + offset_rotated[1], settings.stick_head_width, settings.stick_head_height, self.angle)

  def get_body_rect(self):
    return Rect(self.pos[0], self.pos[1], settings.player_body_width, settings.player_body_height, self.angle)

  def wall_reflection_speed(self, orig_speed):
    mult = -1 if orig_speed > 0 else 1
    speed = max(min(abs(orig_speed), settings.maxspeed), settings.min_wall_reflection_speed)
    return speed * settings.wall_acc * mult

  def check_walls(self):
    rect1, rect2 = self.get_body_rect(), self.get_stick_head()

    hit_left, hit_right, hit_top, hit_bottom = False, False, False, False
    for corner in [rect1.top_left(), rect1.top_right(), rect1.bottom_left(), rect1.bottom_right(),
    rect2.top_left(), rect2.top_right(), rect2.bottom_left(), rect2.bottom_right()]:
      if corner[0] <= settings.leftwall: hit_left = True
      if corner[0] >= settings.rightwall: hit_right = True
      if corner[1] <= settings.topwall: hit_top = True
      if corner[1] >= settings.bottomwall: hit_bottom = True

    if hit_left and self.xspeed < 0: self.xspeed = self.wall_reflection_speed(self.xspeed)
    if hit_right and self.xspeed > 0: self.xspeed = self.wall_reflection_speed(self.xspeed)
    if hit_top and self.yspeed < 0: self.yspeed = self.wall_reflection_speed(self.yspeed)
    if hit_bottom and self.yspeed > 0: self.yspeed = self.wall_reflection_speed(self.yspeed)

  def draw(self, screen):
    rect = self.get_body_rect()
    pygame.draw.rect(screen, settings.LIGHTRED, pygame.Rect(rect.left(), rect.top(), rect.w, rect.h))

    rect = self.get_stick_head()
    pygame.draw.rect(screen, settings.LIGHTRED, pygame.Rect(rect.left(), rect.top(), rect.w, rect.h))

    rect = self.img.get_rect(center=self.pos)
    screen.blit(self.img, rect)

