
import pygame
import settings
from pygamegame import PygameGame
from player import Player
from ball import Ball

class SingleGame(PygameGame):

  def __init__(self):
    super().__init__()
    self.player1 = Player(settings.player1_color, settings.player1_start_pos)

    self.ball = Ball(settings.ball_start_pos, settings.ball_start_speed)

    self.ball_owner = self.player1
    self.player1.get_ball()

  def timerFired(self, dt):
    if self.isKeyPressed(pygame.K_r):
      self.player1.rotate()  

    dirs_pressed = (self.isKeyPressed(pygame.K_LEFT) + self.isKeyPressed(pygame.K_RIGHT)
        + self.isKeyPressed(pygame.K_UP) + self.isKeyPressed(pygame.K_DOWN))

    if dirs_pressed <= 2:
      if self.isKeyPressed(pygame.K_LEFT) and self.isKeyPressed(pygame.K_DOWN):
        self.player1.adjust_target_angle(45)

      elif self.isKeyPressed(pygame.K_LEFT) and self.isKeyPressed(pygame.K_UP):
        self.player1.adjust_target_angle(315)  

      elif self.isKeyPressed(pygame.K_RIGHT) and self.isKeyPressed(pygame.K_DOWN):  
        self.player1.adjust_target_angle(135)  

      elif self.isKeyPressed(pygame.K_RIGHT) and self.isKeyPressed(pygame.K_UP):
        self.player1.adjust_target_angle(225)

      elif self.isKeyPressed(pygame.K_LEFT):
        self.player1.adjust_target_angle(0)

      elif self.isKeyPressed(pygame.K_DOWN):
        self.player1.adjust_target_angle(90)

      elif self.isKeyPressed(pygame.K_RIGHT):
        self.player1.adjust_target_angle(180)

      elif self.isKeyPressed(pygame.K_UP):
        self.player1.adjust_target_angle(270)

      else:
        assert(dirs_pressed == 0)
        self.player1.adjust_target_angle(0)      

    if self.isKeyPressed(pygame.K_LEFT):
      self.player1.accelerate_left()

    if self.isKeyPressed(pygame.K_RIGHT):
      self.player1.accelerate_right()

    if self.isKeyPressed(pygame.K_UP):
      self.player1.accelerate_up()

    if self.isKeyPressed(pygame.K_DOWN):
      self.player1.accelerate_down()  

    if dirs_pressed == 0:
      self.player1.slow_down()

    self.player1.rotate()
    self.player1.move()

    if self.ball_owner == None:
      self.ball.move()
    else:
      self.ball.set_pos(self.ball_owner.get_ball_pos())

  def redrawAll(self, screen):
    self.player1.draw(screen)
    self.ball.draw(screen)

if __name__ == '__main__':
  game = SingleGame()
  game.run()