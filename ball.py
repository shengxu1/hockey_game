
import pygame
import settings
import util
import math

class Ball(object):
  def __init__(self, start_pos):
    self.pos = start_pos
    self.speed = settings.ball_start_speed # can be a float
    self.angle = settings.ball_starting_angle

    self.color = settings.BLACK
    self.radius = settings.ball_radius

  def move(self):
    self.speed = max(self.speed - settings.ball_slowdown, 0)

    self.xspeed = - int(self.speed * math.cos(math.radians(self.angle)))
    self.yspeed = int(self.speed * math.sin(math.radians(self.angle)))

    self.pos = (self.pos[0] + self.xspeed, self.pos[1] + self.yspeed)

  def set_pos(self, pos):
    self.pos = pos

  def set_velocity(self, speed, angle):
    self.speed = speed
    self.angle = angle

  def draw(self, screen):
    # pygame.draw.rect(screen, settings.LIGHTRED, pygame.Rect(self.pos[0] - 8, self.pos[1] - 13, 16, 26))
    # pygame.draw.circle(screen, settings.LIGHTRED, (self.pos[0] + self.radius, self.pos[1]), self.radius * 2)
    pygame.draw.circle(screen, self.color, self.pos, self.radius)
