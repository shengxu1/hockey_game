1. correct rotation: DONE!
2. 球在杆头: DONE!
3. 人射球
4. 4面墙（位置不在0！），球和墙的collision

5. 人抢到球
6. 人和墙的collision
7. 加球门，能进球，进球重置
8. 第二位player，人和人的collision
9. 加守门员
10. 单机流畅运行：球场，时间，得分效果等
11. 简单设计页面：main page, room, create account, login, instructions

12. 转联机模式
13. 允许4player大场模式
14. 加道具，新模式等


circle rectangle collision detection

人：rectangle（左边到右手），取中间点算playerpos

杆头：rectangle

球：circle

守门员：rectangle

angle系统和方向速度系统是2个并存且互不干扰的系统！

------------------------------------------------------------------------
angle系统：

default angle：
不按键：永远正对着对面（前面），除非playerpos在对方蓝线以内并且球门两边以外，那么朝向球门
按前面，后面，上面，下面，4个diagonal：分别是8个possible target angle
note: 从朝向球门到朝前，也有一个小转

旋转方向：那边angle差小就往哪边转 (比如90度 vs 270度)
可以在旋转中间改变target，所以angle不一定是90的倍数！
如果两边都是180度，那么：
下to上：经过后
上to下：经过后
后to前：经过下
前to后：经过下

------------------------------------------------------------------------

方向速度系统：
x_acc, y_acc

left：negative x_acc
right: positive x_acc
up: negative y_acc
down: positive y_acc

left right一起按：x_acc = 0
up down一起按：y_acc = 0

啥都不按：(yspeed同理)
如果xspeed > 0, 那么 xspeed = max(0, xspeed - friction_acc)
如果xspeed < 0, 那么 xspeed = min(0, xspeed + friction_acc)

速度：xspeed = max (xspeed + x_acc, max_speed), yspeed = max (yspeed + y_acc, max_speed)

球和人：
撞上下的墙：yspeed = - yspeed
撞左右的墙或者门将：xspeed = - xspeed

射球：
有一个固定的总射速，通过angle分摊到ball_xspeed和ball_yspeed
如果player有xspeed和yspeed, ball_xspeed和ball_yspeed需调整（应该不能直接加，maybe算一个差，然后加一部分的差，但不能改变方向，有一个minimum的ball_xspeed和ball_yspeed）

人撞人：
xspeed, yspeed交换！！
不管adjustment!

------------------------------------------------------------------------
collision系统：

通过playerpos和angle算出杆头的中心和球的中心





