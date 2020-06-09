
import pygame
import settings
import util
import math

from util import Circle

class Ball(object):
  def __init__(self, start_pos):
    self.pos = start_pos
    self.speed = settings.shot_speed # can be a float
    self.angle = settings.ball_starting_angle

    self.color = settings.BLACK
    self.radius = settings.ball_radius

  def slowdown(self):
    self.speed = max(self.speed - 1, 0)

  def move(self):
    self.xspeed = - int(self.speed * math.cos(math.radians(self.angle)))
    self.yspeed = int(self.speed * math.sin(math.radians(self.angle)))

    self.pos = (self.pos[0] + self.xspeed, self.pos[1] + self.yspeed)

  def check_walls(self):
    if self.pos[1] <= settings.topwall + self.radius and util.is_up(self.angle):
      self.angle = util.mod_angle(360 - self.angle)

    elif self.pos[1] >= settings.bottomwall - self.radius and util.is_down(self.angle):
      self.angle = util.mod_angle(360 - self.angle)

    if self.pos[0] <= settings.leftwall + self.radius and util.is_left(self.angle):
      self.angle = util.mod_angle(180 - self.angle)

    elif self.pos[0] >= settings.rightwall - self.radius and util.is_right(self.angle):
      self.angle = util.mod_angle(180 - self.angle)

  def set_pos(self, pos):
    self.pos = pos

  def set_velocity(self, speed, angle):
    self.speed = speed
    self.angle = angle

  def get_circle(self):
    return Circle(self.pos[0], self.pos[1], self.radius)

  def draw(self, screen):
    # pygame.draw.rect(screen, settings.LIGHTRED, pygame.Rect(self.pos[0] - 8, self.pos[1] - 13, 16, 26))
    # pygame.draw.circle(screen, settings.LIGHTRED, (self.pos[0] + self.radius, self.pos[1]), self.radius * 2)
    pygame.draw.circle(screen, self.color, self.pos, self.radius)
