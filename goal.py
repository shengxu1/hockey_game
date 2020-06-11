
import util
import settings
from util import Rect, Side

class Goal(object):

  # when this goal is scored, increment score of the team passed in
  # x is coordinate of left of goal
  def __init__(self, x, team):
    self.rect = Rect.init_from_top_left(x, settings.goal_top, settings.goal_width, settings.goal_height)
    self.team = team
    self.side = team.side

  def in_goal(self, ball):
    if self.side == Side.LEFT: # the goal on the right
      return self.rect.contains_point(ball.pos[0] + ball.radius, ball.pos[1])
    else: # the goal on the left
      return self.rect.contains_point(ball.pos[0] - ball.radius, ball.pos[1])

  def out_of_bounds(self, ball):
    ball_pos = ball.get_next_position()
    return self.rect.out_of_bounds(ball_pos[0], ball_pos[1])

  def increment_score(self):
    self.team.increment_score()


  