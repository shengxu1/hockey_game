
import pygame
import math
import settings
from enum import Enum 

class Side(Enum):
  LEFT = "left"
  RIGHT = "right"

class Circle(object):
  # (x, y) is coordinate of the circle center, r is radius
  def __init__(self, x, y, r):
    self.x = x
    self.y = y
    self.r = r

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def dot(self, other):
    return self.x * other.x + self.y * other.y

  def length_sqr(self):
    return self.x * self.x + self.y * self.y

  def scalar_prod(self, prod):
    return Point(self.x * prod, self.y * prod)

  # project this vector onto another vector
  def projection(self, other):
    return other.scalar_prod(self.dot(other)/other.length_sqr())

class Rect(object):
  # (x, y) is coordinate of the rectangle center
  def __init__(self, x, y, w, h, angle = 0):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.angle = angle

  # (x, y) is coordinate of the rectangle top left
  @classmethod
  def init_from_top_left(cls, rx, ry, w, h, angle = 0):
    return cls(rx + w / 2, ry + h / 2, w, h, angle)

  def contains_point(self, x, y):
    return self.left() <= x and x <= self.right() and self.top() <= y and y <= self.bottom()

  def out_of_bounds(self, x, y):
    return self.left() >= x or self.right() <= x or self.top() >= y or self.bottom() <= y

  def left(self): return self.x - self.w / 2
  def right(self): return self.x + self.w / 2
  def top(self): return self.y - self.h / 2
  def bottom(self): return self.y + self.h / 2

  # the functions above assume self.angle == 0
  def contains_point_slanted(self, point):
    if self.angle == 0: return self.contains_point(point.x, point.y)

    AB = self.top_right() - self.top_left()
    BC = self.bottom_right() - self.top_right()
    AM = point - self.top_left()
    BM = point - self.top_right()

    return 0 <= AB.dot(AM) <= AB.dot(AB) and 0 <= BC.dot(BM) <= BC.dot(BC)

  def contains_vertex(self, other_rect):
    for vtx in other_rect.get_vertices():
      if self.contains_point_slanted(vtx): return True
    return False
  
  # since we check continuously and the player rects are of the same size, we avoid the edge case of 2 rects intersecting but
  # not containing each other's vertices
  def intersects_rect(self, other_rect):
    return self.contains_vertex(other_rect) or other_rect.contains_vertex(self)

  def get_point(self, offset_x, offset_y):
    offset = pygame.Vector2(offset_x, offset_y)
    offset_rotated = offset.rotate(self.angle)
    return Point(self.x + offset_rotated[0], self.y + offset_rotated[1])

  def get_vertices(self): return [self.top_left(), self.top_right(), self.bottom_left(), self.bottom_right()]

  def top_left(self): return self.get_point(- self.w / 2, - self.h / 2)
  def top_right(self): return self.get_point(self.w / 2, - self.h / 2)
  def bottom_left(self): return self.get_point(- self.w / 2, self.h / 2)
  def bottom_right(self): return self.get_point(self.w / 2, self.h / 2)  

def slow_down(speed, acc):
  if speed < 0:
    return min(speed + acc, 0)
  elif speed > 0:
    return max(speed - acc, 0)
  return speed

# Assumes rectangle is rotated around its center
def slanted_rect_circle_collision(rect, circle):
  offset = pygame.Vector2(circle.x - rect.x, circle.y - rect.y)
  # spin the circle by reverse angle to get to standard axis
  offset_rotated = offset.rotate(-rect.angle)
  rotated_cx, rotated_cy = rect.x + offset_rotated[0], rect.y + offset_rotated[1]
  return rect_circle_collision(rect, Circle(rotated_cx, rotated_cy, circle.r))

def rect_circle_collision(rect, circle):

  # set defaults. Default is when circle center is within rectangle
  testx, testy = circle.x, circle.y

  if circle.x < rect.left(): testx = rect.left() # center to left of rectangle
  elif circle.x > rect.right(): testx = rect.right() # center to right of rectangle

  if circle.y < rect.top(): testy = rect.top() # center to top of rectangle
  elif circle.y > rect.bottom(): testy = rect.bottom() # center to bottom of rectangle

  dist = math.sqrt((circle.x - testx) ** 2 + (circle.y - testy) ** 2)

  return dist <= circle.r

def circle_circle_collision(pos1, radius1, pos2, radius2):
  dist = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
  return dist <= radius1 + radius2

def mod_angle(angle):
  if angle < 0: return angle + 360
  elif angle >= 360: return angle - 360
  return angle

def is_left(angle):
  assert(0 <= angle and angle < 360)
  return angle < 90 or 270 < angle

def is_right(angle):
  return 90 < angle and angle < 270

def is_vertical(angle):
  return angle == 90 or angle == 270

def is_up(angle):
  return 180 < angle and angle < 360

def is_down(angle):
  return 0 < angle and angle < 180

def two_digit_num_to_str(num):
  tens = num // 10
  digit = num % 10
  return str(tens), str(digit)

def to_minute_form(total_seconds):
  return total_seconds // 60, total_seconds % 60

def get_angle_from_quadrant(angle, x, y):
  if x <= 0 and y >= 0: return angle
  if x >= 0 and y >= 0: return 180 - angle
  if x >= 0 and y <= 0: return 180 + angle
  if x <= 0 and y <= 0: return 360 - angle

def in_enemy_region_top(side, pos):
  if side == Side.RIGHT:
    return pos[0] <= settings.left_blue_line and pos[1] <= settings.goal_top
  else:
    return pos[0] >= settings.right_blue_line and pos[1] <= settings.goal_top

def in_enemy_region_bottom(side, pos):
  if side == Side.RIGHT:
    return pos[0] <= settings.left_blue_line and pos[1] >= settings.goal_bottom
  else:
    return pos[0] >= settings.right_blue_line and pos[1] >= settings.goal_bottom

def get_default_angle(side, pos, inital_angle):
  if in_enemy_region_top(side, pos):
    return mod_angle(inital_angle + 45) if side == Side.RIGHT else mod_angle(inital_angle - 45)

  elif in_enemy_region_bottom(side, pos):
    return mod_angle(inital_angle - 45) if side == Side.RIGHT else mod_angle(inital_angle + 45)

  else:
    return inital_angle

def get_initial_angle(side):
  if side == Side.LEFT: return 180
  else: return 0
