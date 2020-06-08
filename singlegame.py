
import pygame
import settings
from pygamegame import PygameGame
from player import Player
from ball import Ball

class SingleGame(PygameGame):

  def __init__(self):
    super().__init__()

    self.player1 = Player(settings.player1_color, settings.player1_start_pos, settings.player1_keyconfig)

    self.ball = Ball(settings.ball_start_pos, settings.ball_start_speed)

    self.ball_owner = self.player1

  def keyPressed(self, keyCode, modifier):
    if keyCode == self.player1.shoot_key:
      self.player1.shoot()


  # adjust player target angle and acceleration based on direction keys pressed
  def adjust_player(self, player):
    dirs_pressed = (self.isKeyPressed(player.left_key) + self.isKeyPressed(player.right_key)
        + self.isKeyPressed(player.up_key) + self.isKeyPressed(player.down_key))

    if dirs_pressed <= 2:
      if self.isKeyPressed(player.left_key) and self.isKeyPressed(player.down_key):
        player.adjust_target_angle(45)

      elif self.isKeyPressed(player.left_key) and self.isKeyPressed(player.up_key):
        player.adjust_target_angle(315)  

      elif self.isKeyPressed(player.right_key) and self.isKeyPressed(player.down_key):  
        player.adjust_target_angle(135)  

      elif self.isKeyPressed(player.right_key) and self.isKeyPressed(player.up_key):
        player.adjust_target_angle(225)

      elif self.isKeyPressed(player.left_key):
        player.adjust_target_angle(0)

      elif self.isKeyPressed(player.down_key):
        player.adjust_target_angle(90)

      elif self.isKeyPressed(player.right_key):
        player.adjust_target_angle(180)

      elif self.isKeyPressed(player.up_key):
        player.adjust_target_angle(270)

      else:
        assert(dirs_pressed == 0)
        player.adjust_target_angle(0)      

    if self.isKeyPressed(player.left_key):
      player.accelerate_left()

    if self.isKeyPressed(player.right_key):
      player.accelerate_right()

    if self.isKeyPressed(player.up_key):
      player.accelerate_up()

    if self.isKeyPressed(player.down_key):
      player.accelerate_down()  

    if dirs_pressed == 0:
      player.slow_down()

  def timerFired(self, dt):
    if not self.player1.is_shooting():
      self.adjust_player(self.player1)
      
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