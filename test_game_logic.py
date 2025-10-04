import pong_game

def test_player_paddle_collision():
    """
    Tests that the ball correctly collides with the player's paddle.
    The test simulates a scenario where the ball is at the edge of the paddle,
    which should trigger a collision.
    """
    # 1. Setup game state for the test
    game_config = {
        'width': 800,
        'height': 600,
        'ball_radius': 10,
        'paddle_width': 10,
        'paddle_height': 100
    }

    # Ball is moving left and is at the edge of the player paddle
    ball = pong_game.Ball(x=20, y=300, radius=10, speed=5)
    ball.vx = -5

    player_paddle = pong_game.Paddle(x=0, y=250, width=10, height=100, speed=7)
    ai_paddle = pong_game.Paddle(x=790, y=250, width=10, height=100, speed=7)

    # 2. Call the collision handler
    pong_game.handle_collisions(ball, player_paddle, ai_paddle, game_config)

    # 3. Assert that the ball's direction is reversed
    assert ball.vx > 0, "Ball should have bounced off the player paddle"

if __name__ == '__main__':
    test_player_paddle_collision()
    print("Test finished.")