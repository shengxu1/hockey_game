
import pygame
import settings
import util

class Ball(object):
  def __init__(self, start_pos, start_speed):
    self.pos = start_pos
    self.xspeed, self.yspeed = start_speed

    self.color = settings.BLACK
    self.radius = settings.ball_radius

  def move(self):
    self.xspeed = util.slow_down(self.xspeed, settings.xacc)
    self.yspeed = util.slow_down(self.yspeed, settings.yacc)

    self.pos = (self.pos[0] + self.xspeed, self.pos[1] + self.yspeed)

  def set_pos(self, pos):
    self.pos = pos

  def draw(self, screen):
    pygame.draw.circle(screen, self.color, self.pos, self.radius)