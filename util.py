
import pygame
import math

class Circle(object):
  # (x, y) is coordinate of the circle center, r is radius
  def __init__(self, x, y, r):
    self.x = x
    self.y = y
    self.r = r

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

  def left(self): return self.x - self.w / 2
  def right(self): return self.x + self.w / 2
  def top(self): return self.y - self.h / 2
  def bottom(self): return self.y + self.h / 2

  def get_point(self, offset_x, offset_y):
    offset = pygame.Vector2(offset_x, offset_y)
    offset_rotated = offset.rotate(self.angle)
    return self.x + offset_rotated[0], self.y + offset_rotated[1]

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

def is_up(angle):
  return 180 < angle and angle < 360

def is_down(angle):
  return 0 < angle and angle < 180

def get_angle_from_quadrant(angle, x, y):
  if x <= 0 and y >= 0: return angle
  if x >= 0 and y >= 0: return 180 - angle
  if x >= 0 and y <= 0: return 180 + angle
  if x <= 0 and y <= 0: return 360 - angle
