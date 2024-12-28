import sys
import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Game state variables
window_width = 800
window_height = 600
shotted_balls = []
firing_balls = []
canon_angle = 0
crossed_ball = 0
game_over = False
balls_from_left = True  # Toggle direction of balls
spawned_ball = 0
score = 0
lives = 3  # Initialize with 3 lives
special_balls = []  # List to store special balls



# Ball class (for moving circles)
class Ball:
    def __init__(self, x, y, x_speed, y_speed):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

class SpecialBall(Ball):
    def __init__(self, x, y, x_speed, y_speed):
        super().__init__(x, y, x_speed, y_speed)


#fired_ball class (for circular projectiles)
class fired_ball:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)  # Convert angle to radians
        self.speed = 3  # Bullet speed

    def move(self):
        # Move the bullet in the direction the cannon is facing
        # The bullet will move along the angle in 2D space
        self.x += self.speed * math.sin(self.angle)  # Horizontal movement based on angle
        self.y += self.speed * math.cos(self.angle)  # Vertical movement based on angle
 # Vertical movement based on angle




# Function to draw a circle using the Midpoint Circle Algorithm
def draw_circle(ball):
    glColor3f(1.0, 1.0, 1.0)  # Set the color to white
    glBegin(GL_POINTS)

    radius = 20  # Radius of the circle
    x_center, y_center = int(ball.x), int(ball.y)
    x = 0
    y = radius
    p = 1 - radius

    # Plot the initial points
    while x <= y:
        # Plot the symmetric points
        glVertex2f(x_center + x, y_center + y)
        glVertex2f(x_center - x, y_center + y)
        glVertex2f(x_center + x, y_center - y)
        glVertex2f(x_center - x, y_center - y)
        glVertex2f(x_center + y, y_center + x)
        glVertex2f(x_center - y, y_center + x)
        glVertex2f(x_center + y, y_center - x)
        glVertex2f(x_center - y, y_center - x)

        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

    glEnd()

def draw_special_ball(ball):
    # Draw red outline
    glColor3f(1.0, 0.0, 0.0)  
    glBegin(GL_POINTS)
    
    radius = 20  # Radius of the special ball
    x_center, y_center = int(ball.x), int(ball.y)
    x = 0
    y = radius
    p = 1 - radius

    while x <= y:
        glVertex2f(x_center + x, y_center + y)
        glVertex2f(x_center - x, y_center + y)
        glVertex2f(x_center + x, y_center - y)
        glVertex2f(x_center - x, y_center - y)
        glVertex2f(x_center + y, y_center + x)
        glVertex2f(x_center - y, y_center + x)
        glVertex2f(x_center + y, y_center - x)
        glVertex2f(x_center - y, y_center - x)

        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

    glEnd()



# Function to draw a fired_ball (small circle) using the Midpoint Circle Algorithm
def draw_fired_ball(fired_ball):
    glColor3f(0.0, 1.0, 0.0)  # Set the color to green
    glBegin(GL_POINTS)

    radius = 7  # Radius of the fired_ball ball
    x_center, y_center = int(fired_ball.x), int(fired_ball.y)
    x = 0
    y = radius
    p = 1 - radius

    # Plot the initial points
    while x <= y:
        # Plot the symmetric points
        glVertex2f(x_center + x, y_center + y)
        glVertex2f(x_center - x, y_center + y)
        glVertex2f(x_center + x, y_center - y)
        glVertex2f(x_center - x, y_center - y)
        glVertex2f(x_center + y, y_center + x)
        glVertex2f(x_center - y, y_center + x)
        glVertex2f(x_center + y, y_center - x)
        glVertex2f(x_center - y, y_center - x)

        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

    glEnd()

# Function to draw the shooter
def draw_shooter():
    glPushMatrix()
    glTranslatef(0, -window_height // 2 + 50, 0)
    glRotatef(canon_angle, 0, 0, 1)

    # Rocket body
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(-20, 0)
    glVertex2f(20, 0)
    glVertex2f(20, 100)
    glVertex2f(-20, 100)
    glEnd()

    # Rocket tip
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(-20, 100)
    glVertex2f(20, 100)
    glVertex2f(0, 130)
    glEnd()

    glPopMatrix()


# Display function
def display():
    global game_over,score

    glClear(GL_COLOR_BUFFER_BIT)

    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(-50, 0)
        for c in "Game Over":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        glutSwapBuffers()
        return

    # Draw all circles (horizontally moving objects)
    for ball in shotted_balls:
        draw_circle(ball)
    
    for ball in special_balls:
        draw_special_ball(ball)
    

    # Draw all firing_balls
    for fired_ball in firing_balls:
        draw_fired_ball(fired_ball)

    # Draw the shooter
    draw_shooter()

    draw_text(-window_width // 2 + 10, window_height // 2 - 30, f"Score: {score}", (1.0, 1.0, 0.0))
    # Draw lives
    draw_text(-window_width // 2 + 10, window_height // 2 - 50, f"Lives: {lives}", (1.0, 0.0, 0.0))  # Display lives in red

    glutSwapBuffers()

def draw_text(x, y, text, color):
    glColor3f(*color)  # Set text color
    glRasterPos2f(x, y)  # Set position
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Update function for animation
def update(value):
    global crossed_ball, game_over, firing_balls, shotted_balls, balls_from_left, spawned_ball, score, lives,canon_angle

    if game_over:
        return

    # Move normal balls and check collisions or boundary crossing
    for ball in shotted_balls[:]:
        ball.move()
        cannon_base_x = 0
        cannon_base_y = -window_height // 2 + 50
        radius_ball = 20
        distance_to_cannon = math.sqrt((ball.x - cannon_base_x) ** 2 + (ball.y - cannon_base_y) ** 2)

        # Game over if a ball hits the cannon base
        if distance_to_cannon <= radius_ball + 50:
            game_over = True
            return

        # Remove balls that cross the screen
        if ball.x > window_width // 2 or ball.x < -window_width // 2 or ball.y > window_height // 2 or ball.y < -window_height // 2:
            shotted_balls.remove(ball)
            crossed_ball += 1
            spawned_ball -= 1

    # Move special balls and handle collisions
    for ball in special_balls[:]:
        ball.move()
        if ball.x > window_width // 2 or ball.x < -window_width // 2 or ball.y > window_height // 2 or ball.y < -window_height // 2:
           special_balls.remove(ball)
        for fired_ball in firing_balls[:]:  
            radius_special_ball = 20
            radius_fired_ball = 7
            distance = math.sqrt((ball.x - fired_ball.x) ** 2 + (ball.y - fired_ball.y) ** 2)
            if distance <= radius_special_ball + radius_fired_ball:
                firing_balls.remove(fired_ball)
                special_balls.remove(ball)
                lives -= 1  # Decrease life when hitting special ball
                if lives <= 0:
                    game_over = True
                break

    # Spawn special balls occasionally
    if random.random() < 0.2 and len(special_balls) < 1:  # 20% chance each update
        if balls_from_left:
            new_special_ball = SpecialBall(-window_width // 2, random.randint(50, window_height // 2 - 50), random.uniform(0.5, 1.0), 0)
        else:
            new_special_ball = SpecialBall(window_width // 2, random.randint(50, window_height // 2 - 50), random.uniform(-1.0, -0.5), 0)
        special_balls.append(new_special_ball)

    # Move fired balls
    for fired_ball in firing_balls[:]:
        # fired_ball.move()
        fired_ball.x += math.sin(math.radians(-canon_angle)) * 5
        fired_ball.y += math.cos(math.radians(-canon_angle)) * 5
        for ball in shotted_balls[:]:
            radius_ball = 20
            radius_fired_ball = 7
            distance = math.sqrt((ball.x - fired_ball.x) ** 2 + (ball.y - fired_ball.y) ** 2)
            if distance <= radius_ball + radius_fired_ball:
                firing_balls.remove(fired_ball)
                shotted_balls.remove(ball)
                score += 1
                break

        # Remove fired balls that leave the screen
        if fired_ball.y > window_height // 2 or fired_ball.x < -window_width // 2 or fired_ball.x > window_width // 2:
            firing_balls.remove(fired_ball)

    # Check for game over due to missed balls
    if crossed_ball >= 5:
        game_over = True

    # Add new balls alternating sides
    if spawned_ball < 5:
        if random.random() < 0.02:
            if balls_from_left:
                new_ball = Ball(-window_width // 2, random.randint(50, window_height // 2 - 50), random.uniform(0.5, 1.0), 0)
            else:
                new_ball = Ball(window_width // 2, random.randint(50, window_height // 2 - 50), random.uniform(-1.0, -0.5), 0)
            shotted_balls.append(new_ball)
            spawned_ball += 1
    else:
        balls_from_left = not balls_from_left
        spawned_ball = 0

    # Update the screen
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# Mouse input for shooter rotation
def mouse(button, state, x, y):
    global canon_angle
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if canon_angle < 90:  # Ensure the shooter doesn't bend further right than +90 degrees
            canon_angle += 10
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if canon_angle > -90:  # Ensure the shooter doesn't bend further left than -90 degrees
            canon_angle -= 10
    glutPostRedisplay()

def keyboard(key, x, y):
    global canon_angle, firing_balls

    # Shooter's base coordinates
    shooter_base_x = 0
    shooter_base_y = -window_height // 2 + 50  
    # Offset to adjust the fired_ball's origin
    offset_x = 0  # Adjust this to control horizontal offset
    offset_y = 0  # Adjust this to control vertical offset

    # Calculate the origin point for the fired_ball based on the canon_angle
    triangle_tip_x = shooter_base_x + math.sin(math.radians(canon_angle)) * (-130 + offset_x)
    triangle_tip_y = shooter_base_y + math.cos(math.radians(canon_angle)) * (130 + offset_y)

    if key == b' ':
        # Fire a fired_ball in the direction the cannon is facing
        new_fired_ball = fired_ball(triangle_tip_x, triangle_tip_y, canon_angle)
        firing_balls.append(new_fired_ball)

    # Update the display
    glutPostRedisplay()


# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-window_width // 2, window_width // 2, -window_height // 2, window_height // 2)

# Main function for Level 2
def main():
    print("Welcome to Level 2!")  # This message can be shown to the player

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Cannon Game - Level 2")

    init()

    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)  # Register keyboard input
    glutTimerFunc(20, update, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
