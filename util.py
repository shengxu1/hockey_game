
import math

def slow_down(speed, acc):
  if speed < 0:
    return min(speed + acc, 0)
  elif speed > 0:
    return max(speed - acc, 0)
  return speed

# rx, ry is center of rectangle, rangle is angle of rectangle. Assumes rectangle is rotated around its center
def slanted_rect_circle_collision(rx, ry, rw, rh, rangle, cx, cy, radius):
  offset = pygame.Vector2(cx - rx, cy - ry)
  # spin the circle by reverse angle to get to standard axis
  offset_rotated = offset.rotate(-rangle)
  rotated_cx, rotated_cy = rx + offset_rotated[0], ry + offset_rotated[1]
  return rect_circle_collision(rx, ry, rw, rh, rotated_cx, rotated_cy, radius)

def rect_circle_collision(rx, ry, rw, rh, cx, cy, radius):
  left, right, top, bottom = rx - rw / 2, rx + rw / 2, ry - rh / 2, ry + rh / 2

  # set defaults. Default is when circle center is within rectangle
  testx, testy = cx, cy

  if cx < left: testx = left # center to left of rectangle
  elif cx > right: testx = right # center to right of rectangle

  if cy < top: testy = top # center to top of rectangle
  elif cy > bottom: testy = bottom # center to bottom of rectangle

  dist = math.sqrt((cx - testx) ** 2 + (cy - testy) ** 2)

  return dist <= radius

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

