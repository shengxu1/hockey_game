
import pygame
import settings
from enum import Enum 

class Direction(Enum):
    STATIONARY = 0
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2

class Player(object):
  def __init__(self, color, start_pos):
    self.orig_img = pygame.transform.scale(pygame.image.load(
      'images/%s-1.png' % color).convert_alpha(), settings.player_size)
    self.img = self.orig_img

    self.xspeed, self.yspeed = 0, 0
    self.xpos, self.ypos = start_pos

    self.angle, self.target_angle = 0, 0
    self.direction = Direction.STATIONARY

  def mod_angle(self, angle):
    if angle < 0: return angle + 360
    elif angle >= 360: return angle - 360
    return angle  

  def rotate_angle(self):

    if self.direction == Direction.CLOCKWISE:
      self.angle = self.mod_angle(self.angle - settings.rot_speed)

    elif self.direction == Direction.COUNTERCLOCKWISE:
      self.angle = self.mod_angle(self.angle + settings.rot_speed)

  def rotate(self):
    if self.direction == Direction.STATIONARY: return

    self.rotate_angle()
    self.img = pygame.transform.rotate(self.orig_img, self.angle)

    if self.angle == self.target_angle: 
      self.direction = Direction.STATIONARY

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

    clockwise_angle = self.mod_angle(self.angle - self.target_angle)
    counterclockwise_angle = self.mod_angle(self.target_angle - self.angle)

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
    if self.xspeed < 0:
      self.xspeed = min(self.xspeed + settings.xacc, 0)
    elif self.xspeed > 0:
      self.xspeed = max(self.xspeed - settings.xacc, 0)
    if self.yspeed < 0:
      self.yspeed = min(self.yspeed + settings.yacc, 0)
    elif self.yspeed > 0:
      self.yspeed = max(self.yspeed - settings.yacc, 0)

  def move(self):
    self.xpos += self.xspeed
    self.ypos += self.yspeed

    # TODO: when close to goal, adjust angle

  def draw(self, screen):
    rect = self.img.get_rect(center=(self.xpos, self.ypos))
    screen.blit(self.img, rect)