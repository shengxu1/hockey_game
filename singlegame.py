
import pygame
import settings
import util
from pygamegame import PygameGame
from player import Player
from ball import Ball

class SingleGame(PygameGame):

  def __init__(self):
    super().__init__()
    self.time = 0

    self.player1 = Player(settings.player1_color, settings.player1_start_pos, settings.player1_keyconfig)

    self.ball = Ball(settings.ball_start_pos)

    self.ball_owner = None

    self.player_shooting = None #at most 1 player can own the ball, so only he can be shooting

  def keyPressed(self, keyCode, modifier):
    if keyCode == self.player1.shoot_key:
      self.player1.shoot()

      if self.ball_owner == self.player1:
        self.ball_owner = None
        self.ball.set_velocity(self.player1.get_speed(), self.player1.angle)
        self.player_shooting = self.player1

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

  def ball_player_collision(self, player):
    if self.player_shooting == player: return

    # collision between ball and stick head (represented by a circle)
    if (util.circle_circle_collision(self.ball.pos, self.ball.radius, 
      player.get_stick_head_pos(), player.stick_head_radius)):

      if player.is_swinging():
        self.ball_owner = None
        # TODO: shooting speed depends on player speed
        self.ball.set_velocity(settings.shot_speed, player.shoot_angle)
      else:
        # TODO: if shifting ball between players, impose a timeout to avoid constant shifting
        self.ball_owner = player
        self.ball.set_velocity(0, 0)

  def process_collisions(self):
    # collision between ball and player stick
    self.ball_player_collision(self.player1)

    # collision between ball and player body
    if util.slanted_rect_circle_collision(self.player1.get_body_rect(), self.ball.get_circle()):
      self.ball_owner = self.player1
      self.ball.set_velocity(0, 0)

    # collision between ball and wall
    self.ball.check_walls()

    # collision between player and wall
    self.player1.check_walls()

    # collision between player and player

    # collision between ball and goalie    

  def timerFired(self, dt):
    self.time += 1
    if not self.player1.is_swinging():
      self.adjust_player(self.player1)
      
    self.player1.rotate()
    self.player1.move()

    if self.ball_owner == None:
      if self.time % settings.ball_slowdown_interval == 0:
        self.ball.slowdown()
      self.ball.move()
    else:
      self.ball.set_pos(self.ball_owner.get_ball_pos())

    self.process_collisions()  

    if self.player_shooting != None and self.player_shooting.finished_swinging():
      self.ball.set_velocity(settings.shot_speed, self.player1.shoot_angle)
      self.player_shooting = None

  def redrawAll(self, screen):
    self.player1.draw(screen)
    self.ball.draw(screen)

if __name__ == '__main__':
  game = SingleGame()
  game.run()