
import pygame
import settings
import util
from enum import Enum 
from goal import Goal
from team import Team, Side
from pygamegame import PygameGame
from player import Player
from ball import Ball
from goalie import Goalie
from util import Rect

class GameState(Enum):
  ONGOING = 0
  PAUSED = 1
  GOALSCORED = 2
  FINISHED = 3

class SingleGame(PygameGame):

  def __init__(self):
    super().__init__()
    self.time = 0

    # self.field_img = pygame.transform.scale(pygame.image.load("images/field.png").convert_alpha(), settings.field_size)

    player1 = Player(settings.player1_color, settings.player1_keyconfig, settings.player1_start_pos, settings.player1_angle)
    player2 = Player(settings.player2_color, settings.player2_keyconfig, settings.player2_start_pos, settings.player2_angle)
    self.players = [player1, player2]

    goalie1 = Goalie(settings.goalie1_startx, settings.goalie_starty, Side.RIGHT, "red", settings.goalie1_keyconfig)
    goalie2 = Goalie(settings.goalie2_startx, settings.goalie_starty, Side.LEFT, "blue", settings.goalie2_keyconfig)
    self.goalies = [goalie1, goalie2]

    self.ball = Ball(settings.ball_start_pos)
    self.left_team = Team(Side.LEFT) # left team attacks right goal
    self.right_team = Team(Side.RIGHT) # right team attacks left goal
    self.goals = [Goal(0, self.right_team), Goal(settings.rightwall, self.left_team)]

    self.kickoff()

  def kickoff(self):
    self.state = GameState.ONGOING
    self.goal_scored_countdown = 0
    self.goal_scored = None

    self.ball.reinit(settings.ball_start_pos)
    self.ball_owner = None
    self.player_shooting = None #at most 1 player can own the ball, so only he can be shooting

  def rekickoff(self):
    for player in self.players:
      player.reinit()
    for goalie in self.goalies:
      goalie.reinit()
    self.kickoff()

  def keyPressed(self, keyCode, modifier):
    for player in self.players:
      if keyCode == player.shoot_key:
        player.shoot()

        if self.ball_owner == player:
          self.ball.set_velocity(self.ball_owner.get_speed(), self.ball_owner.angle)
          self.player_shooting = self.ball_owner
          self.ball_owner = None

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
        player.to_default_angle()      

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
    if (util.slanted_rect_circle_collision(player.get_stick_head(), self.ball.get_circle())):

      if player.is_swinging():
        if self.ball_owner != None: self.ball_owner.lose_ball()
        self.ball_owner = None
        shot_speed, shot_angle = player.get_shot_velocity()
        self.ball.set_velocity(shot_speed, shot_angle)
      else:
        if self.ball_owner != None: self.ball_owner.lose_ball()
        self.ball_owner = player
        self.ball.set_velocity(0, 0)

    # collision between ball and player body
    elif util.slanted_rect_circle_collision(player.get_body_rect(), self.ball.get_circle()):
      if self.ball_owner != None: self.ball_owner.lose_ball()
      self.ball_owner = player
      self.ball.set_velocity(0, 0)

  def process_ball_collisions(self):
    # collision between ball and player stick
    for player in self.players:
      if self.ball_owner != player and player.can_capture():
        self.ball_player_collision(player)

    # collision between ball and walls
    self.ball.check_walls()

    # collision between ball and goalie
    for goalie in self.goalies:
      if util.rect_circle_collision(goalie.get_rect(), self.ball.get_circle()):
        if self.ball_owner != None: self.ball_owner.lose_ball()
        self.ball_owner = None
        angle = goalie.get_reflect_angle(self.ball.angle)
        self.ball.set_velocity(settings.goalie_reflection_speed, angle)

  def check_goal_scored(self):
    for goal in self.goals:
      if goal.in_goal(self.ball):
        self.goal_scored = goal
        goal.increment_score()
        return True
    return False

  def process_goal_scored(self):
    self.state = GameState.GOALSCORED
    self.goal_scored_countdown = settings.goal_scored_countdown

    if self.ball_owner != None:
      self.ball.set_velocity(self.ball_owner.get_speed(), self.ball_owner.angle)
      self.ball_owner.lose_ball()

    self.ball.speed = min(self.ball.speed, settings.max_speed_into_goal)

    self.ball_owner = None

  def process_collisions(self):
    if self.state == GameState.GOALSCORED:
      if self.goal_scored.out_of_bounds(self.ball):
        self.ball.set_velocity(0, 0)

      self.goal_scored_countdown -= 1
      if self.goal_scored_countdown == 0:
        self.rekickoff()
        return

    elif self.check_goal_scored():
      self.process_goal_scored()
    else:
      self.process_ball_collisions()

    # collision between player body and player body
    for i in range(len(self.players)):
      for j in range(i+1, len(self.players)):
        player, otherplayer = self.players[i], self.players[j]
        if player.intersects_player(otherplayer):
          player.exchange_speed(otherplayer)

    # collision between player and wall
    for player in self.players:
      player.check_walls()

  def adjust_goalie(self, goalie):
    if self.isKeyPressed(goalie.up_key):
      goalie.move_up()

    if self.isKeyPressed(goalie.down_key):
      goalie.move_down() 

  def game_loop(self):
    for goalie in self.goalies:
      self.adjust_goalie(goalie)

    for player in self.players:
      if not player.is_swinging():
        self.adjust_player(player)
        
      player.rotate()
      player.move()

    if self.ball_owner == None:
      if self.time % settings.ball_slowdown_interval == 0:
        self.ball.slowdown()
      self.ball.move()
    else:
      self.ball.set_pos(self.ball_owner.get_ball_pos())

    self.process_collisions()  

    if self.player_shooting != None and self.player_shooting.finished_swinging():
      self.player_shooting.lose_ball()
      shot_speed, shot_angle = self.player_shooting.get_shot_velocity()
      self.ball.set_velocity(shot_speed, shot_angle)
      self.player_shooting = None

  def timerFired(self, dt):
    self.time += 1

    if self.state == GameState.ONGOING or self.state == GameState.GOALSCORED:
      self.game_loop()

    for player in self.players:
      player.timer_fired()

  def redrawAll(self, screen):
    # screen.blit(self.field_img, (0, 0))

    pygame.draw.rect(screen, settings.BROWN, pygame.Rect(0, 0, settings.leftwall, settings.canvas_height))
    pygame.draw.rect(screen, settings.BROWN, pygame.Rect(0, 0, settings.canvas_width, settings.topwall))
    pygame.draw.rect(screen, settings.BROWN, pygame.Rect(0, settings.bottomwall, settings.canvas_width, settings.canvas_height - settings.bottomwall))
    pygame.draw.rect(screen, settings.BROWN, pygame.Rect(settings.rightwall, 0, settings.canvas_width - settings.rightwall, settings.canvas_height))

    pygame.draw.rect(screen, settings.LIGHTGREEN, pygame.Rect(0, settings.goal_top, settings.leftwall, settings.goal_height))
    pygame.draw.rect(screen, settings.LIGHTGREEN, pygame.Rect(settings.rightwall, settings.goal_top, settings.canvas_width - settings.rightwall, settings.goal_height))

    for goalie in self.goalies:
      goalie.draw(screen)

    for player in self.players:
      player.draw(screen)  

    self.ball.draw(screen)

if __name__ == '__main__':
  game = SingleGame()
  game.run()