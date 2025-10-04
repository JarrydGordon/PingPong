import pygame
import random
import json

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.vx = random.choice([-speed, speed])
        self.vy = random.choice([-speed, speed])
        self.radius = radius
        self.speed = speed

    def move(self, height):
        self.x += self.vx
        self.y += self.vy

        # Bounce off top and bottom
        if self.y < self.radius or self.y > height - self.radius:
            self.vy *= -1

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.choice([-self.speed, self.speed])
        self.vy = random.choice([-self.speed, self.speed])

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move_up(self):
        """Moves the paddle up, ensuring it doesn't go off-screen."""
        self.y -= self.speed
        if self.y < 0:
            self.y = 0

    def move_down(self, height):
        self.y += self.speed
        if self.y > height - self.height:
            self.y = height - self.height

def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(None, size)
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

def init_game(config):
    WIDTH, HEIGHT = config['window_width'], config['window_height']
    BALL_RADIUS = config['ball_size']
    PADDLE_WIDTH = config['paddle_width']
    PADDLE_HEIGHT = config['paddle_height']
    BALL_SPEED = config['ball_speed']
    PADDLE_SPEED = config['paddle_speed']

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong with AI")
    clock = pygame.time.Clock()

    ball = Ball(WIDTH / 2, HEIGHT / 2, BALL_RADIUS, BALL_SPEED)
    player_paddle = Paddle(0, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
    ai_paddle = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)

    game_config = {
        'width': WIDTH,
        'height': HEIGHT,
        'ball_radius': BALL_RADIUS,
        'paddle_width': PADDLE_WIDTH,
        'fps': 60
    }

    return ball, player_paddle, ai_paddle, screen, clock, game_config

def game_loop(ball, player_paddle, ai_paddle, screen, clock, game_config):
    player_score = 0
    ai_score = 0

    WIDTH = game_config['width']
    HEIGHT = game_config['height']
    BALL_RADIUS = game_config['ball_radius']
    PADDLE_WIDTH = game_config['paddle_width']
    FPS = game_config['fps']

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_paddle.move_up()
        if keys[pygame.K_s]:
            player_paddle.move_down(HEIGHT)

        if ai_paddle.y + ai_paddle.height / 2 < ball.y:
            ai_paddle.move_down(HEIGHT)
        elif ai_paddle.y + ai_paddle.height / 2 > ball.y:
            ai_paddle.move_up()

        ball.move(HEIGHT)

        if (ball.x <= PADDLE_WIDTH and
            ball.y >= player_paddle.y and
            ball.y <= player_paddle.y + player_paddle.height):
            ball.vx *= -1
        elif ball.x <= PADDLE_WIDTH:
            ai_score += 1
            ball.reset(WIDTH / 2, HEIGHT / 2)

        if (ball.x >= WIDTH - PADDLE_WIDTH - BALL_RADIUS and
            ball.y >= ai_paddle.y and
            ball.y <= ai_paddle.y + ai_paddle.height):
            ball.vx *= -1
        elif ball.x >= WIDTH - PADDLE_WIDTH - BALL_RADIUS:
            player_score += 1
            ball.reset(WIDTH / 2, HEIGHT / 2)

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2))
        pygame.draw.rect(screen, WHITE, (player_paddle.x, player_paddle.y, player_paddle.width, player_paddle.height))
        pygame.draw.rect(screen, WHITE, (ai_paddle.x, ai_paddle.y, ai_paddle.width, ai_paddle.height))
        pygame.draw.line(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 1)

        draw_text(screen, str(player_score), 64, WIDTH / 4, 20)
        draw_text(screen, str(ai_score), 64, WIDTH * 3 / 4, 20)

        pygame.display.flip()
        clock.tick(FPS)

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    ball, player_paddle, ai_paddle, screen, clock, game_config = init_game(config)
    game_loop(ball, player_paddle, ai_paddle, screen, clock, game_config)

    pygame.quit()

if __name__ == '__main__':
    main()
