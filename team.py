
class Team(object):

  def __init__(self, side):
    self.score = 0
    self.players = []
    self.side = side

  def add_player(self, player):
    self.players.append(player)

  def players(self):
    return self.players

  def increment_score(self):
    print("SCORE INCREMENTED!")
    self.score += 1