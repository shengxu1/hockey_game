
import pygame
import settings

class Player(object):
  def __init__(self, color):
    self.orig_img = pygame.image.load('images/%s-1.png' % color).convert_alpha()
    self.img = self.orig_img

    self.xspeed, self.yspeed = 0, 0
    self.angle = 0
    self.xpos, self.ypos = 166, 134

  def rotate(self):
    self.angle += settings.delta_angle
    self.img = pygame.transform.rotate(self.orig_img, self.angle)

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

  def draw(self, screen):
    rect = self.img.get_rect(center=(self.xpos, self.ypos))
    screen.blit(self.img, rect)