
import math

def slow_down(speed, acc):
  if speed < 0:
    return min(speed + acc, 0)
  elif speed > 0:
    return max(speed - acc, 0)
  return speed

def rect_circle_collision(rect, cx, cy, radius):
  left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom

  # set defaults. Default is when circle center is within rectangle
  testx, testy = cx, cy

  if cx < left: testx = left # center to left of rectangle
  elif cx > right: testx = right # center to right of rectangle

  if cy < top: testy = top # center to top of rectangle
  elif cy > bottom: testy = bottom # center to bottom of rectangle

  dist = math.sqrt((cx - testx) ** 2 + (cy - testy) ** 2)

  return dist <= radius

def circle_circle_collision(cx1, cy1, radius1, cx2, cy2, radius2):
    dist = math.sqrt((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2)
    return dist <= radius1 + radius2
