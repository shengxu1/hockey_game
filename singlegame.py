
import pygame
import settings
from pygamegame import PygameGame
from player import Player

class SingleGame(PygameGame):

  def __init__(self):
    super().__init__()
    self.player1 = Player("r")

  def timerFired(self, dt):
    if self.isKeyPressed(pygame.K_r):
      self.player1.rotate()  

    no_direction = True

    if self.isKeyPressed(pygame.K_LEFT):
      self.player1.accelerate_left()

    if self.isKeyPressed(pygame.K_RIGHT):
      self.player1.accelerate_right()

    if self.isKeyPressed(pygame.K_UP):
      self.player1.accelerate_up()

    if self.isKeyPressed(pygame.K_DOWN):
      self.player1.accelerate_down()

    if not (self.isKeyPressed(pygame.K_LEFT) or self.isKeyPressed(pygame.K_RIGHT) or
      self.isKeyPressed(pygame.K_UP) or self.isKeyPressed(pygame.K_DOWN)):
      self.player1.slow_down()

    self.player1.move()

  def redrawAll(self, screen):
    self.player1.draw(screen)

if __name__ == '__main__':
  game = SingleGame()
  game.run()