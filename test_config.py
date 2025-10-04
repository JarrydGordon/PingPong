import json
import os
import pong_game

def test_config_loading():
    """
    Tests that the game correctly loads configuration from config.json.
    """
    # 1. Back up the original config file
    with open('config.json', 'r') as f:
        original_config = json.load(f)

    # 2. Modify the config file for the test
    test_config = original_config.copy()
    test_config['ball_size'] = 99
    test_config['paddle_height'] = 150
    with open('config.json', 'w') as f:
        json.dump(test_config, f)

    # 3. Initialize the game with the new config
    with open('config.json', 'r') as f:
        config = json.load(f)

    ball, player_paddle, ai_paddle, screen, clock, config_out = pong_game.init_game(config)

    # 4. Assert that the game settings have changed
    assert ball.radius == 99, f"Ball radius is {ball.radius}, expected 99"
    assert player_paddle.height == 150, f"Paddle height is {player_paddle.height}, expected 150"
    print("Test passed: Game objects are correctly initialized from config.")

    # 5. Restore the original config file
    with open('config.json', 'w') as f:
        json.dump(original_config, f)

if __name__ == "__main__":
    # The test needs a display surface to run, so we need to init pygame.
    import pygame
    pygame.init()
    test_config_loading()
    pygame.quit()