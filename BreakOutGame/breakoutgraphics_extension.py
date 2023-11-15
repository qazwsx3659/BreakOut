"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

Name: Tiffany
File: breakoutgraphics.py
This file produces all objects (ball, paddle, brick, window) used in the breakout clone,
also provides essential parameters to game motions.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random
import pdb

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball
SCORE_PER_BRICK = 10   # score got of breaking per brick


class BreakoutGraphicsExt:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 score_per_brick=SCORE_PER_BRICK, title='Breakout'):
        """
        ToDo:
        1) create all bricks, ball and paddle used in the game
        2) setting the mouse listener
        """
        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self._paddle_offset = paddle_offset
        self.paddle.filled = True
        # === initial x position of the paddle === #
        paddle_x0 = (self.window.width - self.paddle.width)/2
        # === initial y position of the paddle === #
        self._paddle_y0 = self.window.height - (self._paddle_offset + self.paddle.height)
        self.window.add(self.paddle, x=paddle_x0, y=self._paddle_y0)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.ball_x = (self.window.width - self.ball.width)/2
        self.ball_y = (self.window.height - self.ball.height)/2
        self.window.add(self.ball, x=self.ball_x, y=self.ball_y)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize our mouse listeners
        onmouseclicked(self.check_ball_movement)
        onmousemoved(self.paddle_motion)

        # Draw bricks
        self._color_idx = 0
        self.brick_rows = brick_rows
        self.brick_cols = brick_cols
        for i in range(self.brick_rows):
            if i % 2 == 0:
                self._color_idx += 1
            for j in range(self.brick_cols):
                self._brick = GRect(brick_width, brick_height)
                brick_x = j * (brick_width + brick_spacing)
                brick_y = brick_offset + i * (brick_height + brick_spacing)
                self._brick.filled = True
                self.brick_fill_color()
                self.window.add(self._brick, x=brick_x, y=brick_y)

        # add slogan of game start
        self._label = GLabel('')
        self.set_label_slogan()
        self._label_x = (self.window.width - self._label.width) / 2
        self._label_y = (self.ball.y + self.paddle.y) / 2
        self.window.add(self._label, x=self._label_x, y=self._label_y)

        # add lives at the upper left of the window
        self.red = GOval(ball_radius*2, ball_radius*2)
        self.set_oval_color(self.red)
        self.green = GOval(ball_radius*2, ball_radius*2)
        self.set_oval_color(self.green, 'green')
        self.org = GOval(ball_radius*2, ball_radius*2)
        self.set_oval_color(self.org, 'orange')
        space_between = ball_radius/2
        self.window.add(self.green)
        self.window.add(self.org, x=self.green.width + space_between, y=0)
        self.window.add(self.red, x=self.org.x + self.org.width + space_between, y=0)

        # add score label
        self.score = 0
        self._score_max = score_per_brick * brick_cols * brick_rows
        self._max_label = GLabel(f'Score: {self._score_max}')
        self.score_label = GLabel(f'Score: {self.score}')
        self.score_label.font = 'Chiller-20-bold'
        self._max_label.font = 'Chiller-20-bold'
        self.window.add(self.score_label,
                        x=self.window.width - self._max_label.width, y=self.score_label.height*1.2)

    def check_ball_movement(self, _):
        """
        the mouse click listener judges if the ball is static. if yes, setting a velocity.
        """
        ball_static = self.__dx == 0 and self.__dy == 0
        if ball_static:
            self.window.remove(self._label)
            self.set_ball_velocity()

    def set_ball_velocity(self):
        """
        the function sets the initial x and y velocity to the ball
        """
        self.__dy = INITIAL_Y_SPEED
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def ball_x_in_window(self):
        """
        the method judges if the ball is within the width of the window
        :return: boolean
        """
        left_boundary = self.ball.x > 0
        right_boundary = self.ball.x < self.window.width - self.ball.width
        return left_boundary and right_boundary

    def ball_y_in_window(self):
        """
        the method judges if the ball is within the height of the window
        :return: boolean
        """
        top_boundary = self.ball.y > 0
        bottom_boundary = self.ball.y < self.window.height - self.ball.height
        return top_boundary and bottom_boundary

    def get_ball_dx(self):
        """
        the function returns the x velocity of the ball
        :return: float, x velocity of the ball
        """
        return self.__dx

    def get_ball_dy(self):
        """
        the function returns the y velocity of the ball
        :return: float, y velocity of the ball
        """
        return self.__dy

    def paddle_motion(self, event):
        """
        the function defines the paddle motion as mouse moved
        :param event: float, mouse event
        :return: NA
        """
        paddle_x = event.x - self.paddle.width/2

        if paddle_x + self.paddle.width >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
        elif paddle_x < 0:
            self.paddle.x = 0
        else:
            self.paddle.x = paddle_x

        self.paddle.y = self._paddle_y0

    def brick_fill_color(self):
        """
        The function fills the color of all bricks (two rows with one color)
        User can add color with increasing rows
        :return: NA
        """
        color1 = 'red'
        color2 = 'orange'
        color3 = 'yellow'
        color4 = 'green'
        color5 = 'blue'
        if self._color_idx == 1:
            self._brick.fill_color = color1
            self._brick.color = color1
        elif self._color_idx == 2:
            self._brick.fill_color = color2
            self._brick.color = color2
        elif self._color_idx == 3:
            self._brick.fill_color = color3
            self._brick.color = color3
        elif self._color_idx == 4:
            self._brick.fill_color = color4
            self._brick.color = color4
        elif self._color_idx == 5:
            self._brick.fill_color = color5
            self._brick.color = color5

    @classmethod
    def set_oval_color(cls, obj, color='Red'):
        obj.filled = True
        obj.fill_color = color
        obj.color = color

    def set_ball_position(self):
        """
        the function sets the ball to initial position defined in the constructor.
        :return: NA
        """
        self.ball.x = self.ball_x
        self.ball.y = self.ball_y

    def set_ball_static(self):
        """
        the function sets to ball static.
        :return: NA
        """
        self.__dx = 0
        self.__dy = 0

    def get_brick_num(self):
        """
        the function returns the total number of the bricks in this game
        :return: int, total counts of the bricks
        """
        return self.brick_cols * self.brick_rows

    def set_label_slogan(self, words_on_label='Click to start!'):
        """
        the function sets the slogan of the game slogan
        :param words_on_label: str, slogan used in the game
        :return: NA
        """
        self._label.text = words_on_label
        self._label.font = 'Chiller-40-bold'

    def set_label_position(self):
        """
        the function reset the position of the game slogan
        :return: NA
        """
        self._label_x = (self.window.width - self._label.width) / 2
        self._label.x = self._label_x
        self._label.y = self._label_y
        self.window.add(self._label, x=self._label_x, y=self._label_y)

    def renew_score(self):
        """
        the function renew the score after breaking each bricks
        :return: NA
        """
        self.score += SCORE_PER_BRICK
        self.score_label.text = f'Score: {self.score}'

