import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Ball:
    """A class to represent the ball in the Pong game."""
    def __init__(self):
        """
        Initializes the Ball object.

        The ball is initialized at the center of the screen with a random velocity.
        """
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = random.choice([-5, 5])
        self.vy = random.choice([-5, 5])
        self.radius = BALL_RADIUS

    def move(self):
        """
        Moves the ball according to its velocity.

        It also handles bouncing off the top and bottom walls.
        """
        self.x += self.vx
        self.y += self.vy

        # Bounce off top and bottom
        if self.y < self.radius or self.y > HEIGHT - self.radius:
            self.vy *= -1

    def reset(self):
        """Resets the ball to the center of the screen with a new random velocity."""
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = random.choice([-5, 5])
        self.vy = random.choice([-5, 5])

class Paddle:
    """A class to represent a paddle in the Pong game."""
    def __init__(self, x, y):
        """
        Initializes the Paddle object.

        Args:
            x (int): The initial x-coordinate of the paddle.
            y (int): The initial y-coordinate of the paddle.
        """
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = 5

    def move_up(self):
        """Moves the paddle up, ensuring it doesn't go off-screen."""
        self.y -= self.speed
        if self.y < 0:
            self.y = 0

    def move_down(self):
        """Moves the paddle down, ensuring it doesn't go off-screen."""
        self.y += self.speed
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

def draw_text(text, size, x, y):
    """
    Draws text on the screen.

    Args:
        text (str): The text to be displayed.
        size (int): The font size.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.
    """
    font = pygame.font.Font(None, size)
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

def main():
    """
    The main function to run the Pong game.

    This function initializes the game window, objects, and runs the main game loop.
    It handles user input, updates game state, and renders the game on the screen.
    """
    # Create game objects
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong with AI")
    clock = pygame.time.Clock()

    ball = Ball()
    player_paddle = Paddle(0, HEIGHT / 2 - PADDLE_HEIGHT / 2)
    ai_paddle = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2)

    player_score = 0
    ai_score = 0

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_paddle.move_up()
        if keys[pygame.K_s]:
            player_paddle.move_down()

        # AI paddle movement
        if ai_paddle.y + ai_paddle.height / 2 < ball.y:
            ai_paddle.move_down()
        elif ai_paddle.y + ai_paddle.height / 2 > ball.y:
            ai_paddle.move_up()

        # Ball movement
        ball.move()

        # Ball collision with paddles
        if (ball.x <= PADDLE_WIDTH and
            ball.y >= player_paddle.y and
            ball.y <= player_paddle.y + player_paddle.height):
            ball.vx *= -1
        elif ball.x <= PADDLE_WIDTH:
            ai_score += 1
            ball.reset()

        if (ball.x >= WIDTH - PADDLE_WIDTH - BALL_RADIUS and
            ball.y >= ai_paddle.y and
            ball.y <= ai_paddle.y + ai_paddle.height):
            ball.vx *= -1
        elif ball.x >= WIDTH - PADDLE_WIDTH - BALL_RADIUS:
            player_score += 1
            ball.reset()

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (ball.x - BALL_RADIUS, ball.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2))
        pygame.draw.rect(screen, WHITE, (player_paddle.x, player_paddle.y, player_paddle.width, player_paddle.height))
        pygame.draw.rect(screen, WHITE, (ai_paddle.x, ai_paddle.y, ai_paddle.width, ai_paddle.height))
        pygame.draw.line(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 1)

        draw_text(str(player_score), 64, WIDTH / 4, 20)
        draw_text(str(ai_score), 64, WIDTH * 3 / 4, 20)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
