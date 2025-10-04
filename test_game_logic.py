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

def test_player_paddle_edge_collision():
    """
    Tests that the ball correctly collides with the top edge of the player's paddle.
    This test simulates a scenario where the ball's center is slightly above the paddle,
    but its radius causes an overlap, which should trigger a collision.
    """
    game_config = {
        'width': 800,
        'height': 600,
        'ball_radius': 10,
        'paddle_width': 10,
        'paddle_height': 100
    }

    player_paddle = pong_game.Paddle(x=0, y=250, width=10, height=100, speed=7)
    ball = pong_game.Ball(x=20, y=245, radius=10, speed=5)
    ball.vx = -5
    ai_paddle = pong_game.Paddle(x=790, y=250, width=10, height=100, speed=7)

    pong_game.handle_collisions(ball, player_paddle, ai_paddle, game_config)

    assert ball.vx > 0, "Ball should have bounced off the player paddle's edge"

if __name__ == '__main__':
    test_player_paddle_collision()
    test_player_paddle_edge_collision()
    print("All tests finished successfully.")