"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

Name: Tiffany
File name: breakout.py
This program is a breakout clone. Users have 3 lives.
"""

from campy.gui.events.timer import pause
from breakoutgraphics_extension import BreakoutGraphicsExt
from campy.graphics.gobjects import GLabel

# constants
FRAME_RATE = 60         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphicsExt()
    window = graphics.window
    ball = graphics.ball
    paddle = graphics.paddle
    is_bounce_back = False
    r = ball.height / 2  # radius of the ball
    num_lives = NUM_LIVES
    total_brick = graphics.get_brick_num()
    brick_cnt = 0

    # Add the animation loop here!
    while True:
        if not is_bounce_back:
            vx = graphics.get_ball_dx()
            vy = graphics.get_ball_dy()

        ball.move(vx, vy)
        pause(FRAME_RATE)

        for x in (ball.x, ball.x + 2*r):
            for y in (ball.y, ball.y + 2*r):
                obj = window.get_object_at(x, y)
                if obj is not None:
                    is_bounce_back = True
                    if obj == paddle and y == ball.y + 2*r:
                        if vy > 0:  # ball only bounce back at paddle when moving downwards
                            vy = -vy
                        break
                    elif obj != paddle \
                            and obj != graphics.red and obj != graphics.org and obj != graphics.green\
                            and obj != graphics.score_label:
                        window.remove(obj)
                        brick_cnt += 1
                        graphics.renew_score()
                        vy = -vy
                        break
            break

        x_out_of_window = ball.x < 0 or ball.x > window.width - ball.width
        y_out_of_bottom = ball.y > window.height - ball.height
        y_out_of_top = ball.y < 0
        if x_out_of_window:
            is_bounce_back = True
            vx = -vx

        if y_out_of_top:
            is_bounce_back = True
            vy = -vy

        if y_out_of_bottom:
            is_bounce_back = False
            num_lives -= 1
            if num_lives > 0:
                graphics.set_ball_position()
                graphics.set_ball_static()
                graphics.set_label_slogan('Click to restart!')
                graphics.set_label_position()
                if num_lives == NUM_LIVES - 1:
                    window.remove(graphics.green)
                elif num_lives == NUM_LIVES - 2:
                    window.remove(graphics.org)

            else:
                graphics.set_label_slogan('You are dead!')
                graphics.set_label_position()
                window.remove(graphics.red)
                break

        if brick_cnt == total_brick:
            graphics.set_label_slogan('Congrats!')
            graphics.set_label_position()
            break


if __name__ == '__main__':
    main()
