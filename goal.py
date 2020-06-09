
import util
import settings
from util import Rect

class Goal(object):

  # when this goal is scored, increment score of the team passed in
  # x is coordinate of left of goal
  def __init__(self, x, team):
    self.rect = Rect.init_from_top_left(x, settings.goal_top, settings.goal_width, settings.goal_height)
    self.team = team

  def in_goal(self, ball):
    return self.rect.contains_point(ball.pos[0], ball.pos[1])

  def out_of_bounds(self, ball):
    return self.rect.out_of_bounds(ball.pos[0], ball.pos[1])

  def increment_score(self):
    self.team.increment_score()


  