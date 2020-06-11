
import pygame
import settings
import util
from util import Rect, Side

class Goalie(object):

  def __init__(self, x, y, side, color, key_config):
    self.x = x
    self.y = self.starty = y
    self.ymin = settings.goal_top + settings.goalie_height / 3
    self.ymax = settings.goal_bottom - settings.goalie_height / 3
    self.side = side

    self.up_key, self.down_key = key_config

    self.img = pygame.transform.scale(pygame.image.load("images/%s-%s-goalie.png" % (side.value, color)).convert_alpha(), settings.goalie_size)

  def move_down(self):
    if self.y < self.ymax:
      self.y += settings.goalie_speed

  def move_up(self):
    if self.y > self.ymin:
      self.y -= settings.goalie_speed

  def reinit(self):
    self.y = self.starty

  def get_rect(self):
    return Rect(self.x, self.y, settings.goalie_width, settings.goalie_height)

  def get_reflect_angle(self, angle):
    if self.side == Side.LEFT and util.is_left(angle):
      return util.mod_angle(180 - angle)
    if self.side == Side.RIGHT and util.is_right(angle):
      return util.mod_angle(180 - angle)

    if util.is_vertical(angle):
      return 180 if self.side == Side.LEFT else 0

    return angle

  def draw(self, screen):
    # rect = self.get_rect()
    # pygame.draw.rect(screen, settings.LIGHTRED, pygame.Rect(rect.left(), rect.top(), rect.w, rect.h))

    rect = self.img.get_rect(center=(self.x, self.y))
    screen.blit(self.img, rect)

