import sys
import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import level_2  

# Game state variables
window_width = 800
window_height = 600
shotted_balls = []  # shotted_balls
firing_balls = []  # firing_balls
rocket_angle = 0
game_over = False
ball_colors = [(1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0), (1.0, 0.0, 1.0)]  
misses = 0
decrease_countdown = False  # Flag to allow space-triggered countdown
score = 0 

# Ball class for cluster and firing_balls
class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# Function to draw a circle using the Midpoint Circle Algorithm
def draw_circle(x_center, y_center, radius, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius

    def plot_points(xc, yc, x, y):
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        glVertex2f(xc + y, yc + x)
        glVertex2f(xc - y, yc + x)
        glVertex2f(xc + y, yc - x)
        glVertex2f(xc - y, yc - x)


    plot_points(x_center, y_center, x, y)
    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        plot_points(x_center, y_center, x, y)
    glEnd()

# Function to draw a line using the Midpoint Line Algorithm
def draw_line(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        glVertex2f(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    glEnd()


# Updated function to draw a ball
def draw_ball(ball):
    draw_circle(ball.x, ball.y, 20, ball.color)


# Updated function to draw the shooter
def draw_shooter():
    glPushMatrix()
    glTranslatef(0, -window_height // 2 + 50, 0)
    glRotatef(rocket_angle, 0, 0, 1)

    # Rocket body (rectangle)
    draw_line(-20, 0, -20, 100, (0.0, 0.0, 1.0))  # Left vertical
    draw_line(20, 0, 20, 100, (0.0, 0.0, 1.0))   # Right vertical
    draw_line(-20, 0, 20, 0, (0.0, 0.0, 1.0))    # Bottom horizontal
    draw_line(-20, 100, 20, 100, (0.0, 0.0, 1.0))  # Top horizontal

    # Rocket tip (triangle)
    draw_line(-20, 100, 0, 130, (1.0, 0.0, 0.0))  # Left edge
    draw_line(20, 100, 0, 130, (1.0, 0.0, 0.0))   # Right edge
    draw_line(-20, 100, 20, 100, (1.0, 0.0, 0.0))  # Base
    glPopMatrix()

def render_text(x, y, text, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))



# Function to initialize the pyramid of shotted_balls within boundaries
def init_pyramid():
    shotted_balls = []
    base_width = window_width // 2  
    ball_spacing = 40  # Spacing between the shotted_balls
    num_rows = (window_height // 2 - 40) // ball_spacing


    for row in range(num_rows):
        num_balls_in_row = num_rows + row  
        row_width = (num_balls_in_row - 1) * ball_spacing
        x_start = -row_width // 2

        for i in range(num_balls_in_row):
            x = x_start + i * ball_spacing
            y = window_height // 2 - row * ball_spacing - 40
            shotted_balls.append(Ball(x, y, random.choice(ball_colors)))
    return shotted_balls


# Display function
def display():
    global game_over
    glClear(GL_COLOR_BUFFER_BIT)
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(-100, 0)
        for c in "Game Over: 3 Misses":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        glutSwapBuffers()
        return

    for ball in shotted_balls:
        draw_ball(ball)

    for bullet in firing_balls:
        draw_ball(bullet)
    draw_shooter()
    render_text(-window_width // 2 + 20, window_height // 2 - 30, f"Score: {score}", color=(1.0, 1.0, 0.0))

    glutSwapBuffers()

# Update function for animation
def update(value):
    global firing_balls, shotted_balls, game_over, show_congratulations, misses,score

    if game_over:
        return

    for bullet in firing_balls[:]:
        bullet.x += math.sin(math.radians(-rocket_angle)) * 5
        bullet.y += math.cos(math.radians(-rocket_angle)) * 5

        for ball in shotted_balls[:]:
            distance = math.sqrt((bullet.x - ball.x)**2 + (bullet.y - ball.y)**2)
            if distance <= 40:
                firing_balls.remove(bullet)
                shotted_balls.remove(ball)
                score += 1
                break

        if bullet.y > window_height // 2 or bullet.x < -window_width // 2 or bullet.x > window_width // 2:
            firing_balls.remove(bullet)
            misses += 1
            if misses >= 3:
                game_over = True
                glutPostRedisplay()
                return


    if len(shotted_balls) == 0 and not show_congratulations:
        show_congratulations = True
        glutDisplayFunc(display_congratulations_and_countdown)
        glutPostRedisplay()
        return

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

show_congratulations = False
countdown_value = 3

def display_congratulations_and_countdown():
    global decrease_countdown


    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 1.0, 0.0)
    glRasterPos2f(-150, 0)
    for c in "Congratulations! Level 1 Completed":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    glColor3f(1.0, 1.0, 0.0)
    glRasterPos2f(50, -50)
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(str(countdown_value)))
    glutSwapBuffers()
    decrease_countdown = True


def transition_to_level_2():
    global countdown_value, decrease_countdown
    countdown_value = 3
    decrease_countdown = False
    glutLeaveMainLoop()
    import level_2
    level_2.main()

def mouse(button, state, x, y):
    global rocket_angle
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if rocket_angle < 90:
           rocket_angle += 7
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if rocket_angle > -90:
            rocket_angle -= 7
    glutPostRedisplay()


def keyboard(key, x, y):
    global rocket_angle, firing_balls, countdown_value, decrease_countdown


    if key == b' ':
        if decrease_countdown and countdown_value > 0:
            countdown_value -= 1
            print(f"Countdown decreased to: {countdown_value}")
            glutPostRedisplay()
            if countdown_value == 0:
                transition_to_level_2()
        else:
            bullet = Ball(
                0 + math.sin(math.radians(-rocket_angle)) * 130,
                -window_height // 2 + 50 + math.cos(math.radians(-rocket_angle)) * 130,
                (0.0, 1.0, 0.0)
            )
            firing_balls.append(bullet)
   
    glutPostRedisplay()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-window_width // 2, window_width // 2, -window_height // 2, window_height // 2)


def main():
    global shotted_balls
    shotted_balls = init_pyramid()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Bubble Shooter - Level 1")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)
    glutMainLoop()
if __name__ == "__main__":
    main()