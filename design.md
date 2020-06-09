1. correct rotation: DONE!
2. 球在杆头: DONE!
3. 人射球: DONE
4. 4面墙（位置不在0！），球和墙的collision: DONE

球员仅仅是给球施加一个加速度（非常大）！如果球原本就有速度（比如被其他球员带着，那么就是向量之和！）

不仅仅是改变射球速度，还会改变射球方向！！  射门xspeed + player xspeed, 射门yspeed + player yspeed

一旦进入球网，就脱离人的控制，然后继续运动，知道碰到球网边缘停止

5. 人抢到球: 还需身体和球碰撞: DONE
6. 人和墙的collision: DONE
7. 加球门，能进球，进球重置: DONE
8. 第二位player，人和人的collision
9. 加守门员
10. 单机流畅运行：球场，时间，得分效果等
11. 简单设计页面：main page, room, create account, login, instructions

12. 转联机模式
13. 允许4player大场模式
14. 加道具，动画，新模式, AI等


circle rectangle collision detection

人：rectangle（胸前算左边），取中间点算playerpos

杆头：大circle

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
射门期间暂时停止移动！（速度位置都停止不变）
人先摆动, 脱离了球（或者没有球）
人在摆动时，算是射门状态，强制摆动（暂时忽略方向键target angle，target angle为射门前位置）
如果恢复到原位，发现有球（collision), 那么击球成功，球速为挥杆前人的速度
整个摆动过程非常迅速（普通摆动速度试试？但摆动幅度很小，15左右）

球在和杆头前rectangle接触时，若是为射门状态，就被射出，否则就被人掌控
在射门动作时不算和球的collision!, 射门动作结束瞬间再算！

有一个固定的总射速，通过angle分摊到ball_xspeed和ball_yspeed
如果player有xspeed和yspeed, ball_xspeed和ball_yspeed需调整（应该不能直接加，maybe算一个差，然后加一部分的差，但不能改变方向，有一个minimum的ball_xspeed和ball_yspeed）

人撞人：
xspeed, yspeed交换！！
不管adjustment!

------------------------------------------------------------------------
collision系统：

通过playerpos和angle算出杆头的中心和球的中心

Apart from player-player and player-ball, all reflections （守门员，墙） are one-sided!
player-ball: ball speed depends on player speed before 射门，player speed不受影响

player-player: speed交换

player和守门员的碰撞可以忽略！

只用看球和守门员的碰撞，note that ball might be controlled by player! 这时候若是碰到守门员，那么球就脱离掌控。
守门员反弹球的速度恒定，角度取决于球本来x,y speed（若是在球员身上则是球员x, y speed）。如果球员某个speed是0，那么就直线反弹）

为了简洁，4道墙可以看成4个很大的长方形 - pygame.Rect（超出边界那种，先画个丑版的）

所以，不需要知道collide到了某个长方体的哪一边，只需要知道是否collide了








