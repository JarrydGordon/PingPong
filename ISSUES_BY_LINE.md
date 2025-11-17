# PingPong Code Quality Issues - Line-by-Line Breakdown

## Critical Issues (Fix First)

### Line 6: Global pygame.init()
```python
pygame.init()
```
**Issue:** Module-level initialization causes side effects on import
**Severity:** MEDIUM
**Fix:** Move to `main()` function
```python
# Better approach
def main():
    pygame.init()
    # ... rest of code
```

---

### Lines 161-162: Missing Error Handling
```python
with open('config.json', 'r') as f:
    config = json.load(f)
```
**Issue:** No try/except for file or JSON errors
**Severity:** HIGH
**Crashes on:** Missing file, invalid JSON, permission errors
**Fix:**
```python
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: config.json contains invalid JSON")
    sys.exit(1)
```

---

### Lines 60-65: Config Dictionary Access Without Validation
```python
WIDTH, HEIGHT = config['window_width'], config['window_height']
BALL_RADIUS = config['ball_size']
PADDLE_WIDTH = config['paddle_width']
PADDLE_HEIGHT = config['paddle_height']
BALL_SPEED = config['ball_speed']
PADDLE_SPEED = config['paddle_speed']
```
**Issue:** KeyError if any key missing
**Severity:** HIGH
**Fix:**
```python
def validate_config(config):
    required_keys = ['window_width', 'window_height', 'ball_size', 
                     'paddle_width', 'paddle_height', 'ball_speed', 'paddle_speed']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    return config

# In main()
config = validate_config(config)
```

---

## High Complexity Issues

### Lines 85-115: handle_collisions() - CC=9 (Too High)
**Issue:** Complex nested conditionals, duplicated logic
**Severity:** MEDIUM
**Specific Problems:**
- Lines 94-96: Complex collision check for player paddle
- Lines 105-107: Nearly identical collision check for AI paddle
- Mixes collision detection with position adjustment
- Mixes collision detection with scoring

**Current Code:**
```python
# Player paddle collision
if (ball.x - ball.radius <= PADDLE_WIDTH and
    ball.y + ball.radius >= player_paddle.y and
    ball.y - ball.radius <= player_paddle.y + player_paddle.height):
    ball.vx *= -1
    ball.x = PADDLE_WIDTH + ball.radius
```

**Recommended Refactor:**
```python
def check_paddle_collision(ball, paddle, is_left):
    """Check if ball collides with paddle and bounce if needed."""
    if is_left:
        collision = (ball.x - ball.radius <= paddle.x + paddle.width and
                    ball.y + ball.radius >= paddle.y and
                    ball.y - ball.radius <= paddle.y + paddle.height)
        if collision:
            ball.vx *= -1
            ball.x = paddle.x + paddle.width + ball.radius
            return True
    else:
        collision = (ball.x + ball.radius >= paddle.x and
                    ball.y + ball.radius >= paddle.y and
                    ball.y - ball.radius <= paddle.y + paddle.height)
        if collision:
            ball.vx *= -1
            ball.x = paddle.x - ball.radius
            return True
    return False
```

---

### Lines 117-158: game_loop() - CC=8 (Too High)
**Issue:** Too many responsibilities
**Severity:** MEDIUM

**Current Responsibilities:**
1. Event handling (line 127-129)
2. Input processing (lines 131-135)
3. AI movement (lines 137-140)
4. Physics (line 142)
5. Collision detection (line 144)
6. Scoring (lines 145-146)
7. Rendering (lines 148-155)
8. Frame rate (line 158)

**Recommended Refactor:**
```python
def handle_input(player_paddle, height):
    """Process keyboard input for player paddle."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_paddle.move_up()
    if keys[pygame.K_s]:
        player_paddle.move_down(height)

def update_ai(ai_paddle, ball, height):
    """Update AI paddle position."""
    if ai_paddle.y + ai_paddle.height / 2 < ball.y:
        ai_paddle.move_down(height)
    elif ai_paddle.y + ai_paddle.height / 2 > ball.y:
        ai_paddle.move_up()

def render(screen, ball, player_paddle, ai_paddle, player_score, ai_score, game_config):
    """Render all game objects."""
    # Drawing code here
```

---

## Magic Numbers (15+ Instances)

### Lines 71-73: Initial Position Magic Numbers
```python
ball = Ball(WIDTH / 2, HEIGHT / 2, BALL_RADIUS, BALL_SPEED)
player_paddle = Paddle(0, HEIGHT / 2 - PADDLE_HEIGHT / 2, ...)
ai_paddle = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2, ...)
```
**Severity:** HIGH (affects 3 lines, repeated again at 102, 113)
**Fix:**
```python
def calculate_center_y(height, object_height):
    """Calculate centered Y position."""
    return height / 2 - object_height / 2

def init_game(config):
    # ... setup ...
    ball = Ball(WIDTH / 2, HEIGHT / 2, BALL_RADIUS, BALL_SPEED)
    player_paddle = Paddle(0, calculate_center_y(HEIGHT, PADDLE_HEIGHT), ...)
    ai_paddle = Paddle(WIDTH - PADDLE_WIDTH, calculate_center_y(HEIGHT, PADDLE_HEIGHT), ...)
```

---

### Lines 102, 113: Duplicate Ball Reset
```python
ball.reset(WIDTH / 2, HEIGHT / 2)  # Line 102
ball.reset(WIDTH / 2, HEIGHT / 2)  # Line 113
```
**Severity:** MEDIUM (100% duplicate)
**Fix:**
```python
def reset_ball(ball, width, height):
    """Reset ball to center of screen."""
    ball.reset(width / 2, height / 2)

# Usage:
# In handle_collisions, replace both calls with:
reset_ball(ball, WIDTH, HEIGHT)
```

---

### Lines 137, 139: AI Target Magic Number
```python
if ai_paddle.y + ai_paddle.height / 2 < ball.y:
    ai_paddle.move_down(HEIGHT)
elif ai_paddle.y + ai_paddle.height / 2 > ball.y:
    ai_paddle.move_up()
```
**Issue:** Division by 2 is magic (finding center), repeated twice
**Severity:** MEDIUM
**Fix:**
```python
def get_paddle_center_y(paddle):
    """Get Y coordinate of paddle center."""
    return paddle.y + paddle.height / 2

# In game_loop:
paddle_center = get_paddle_center_y(ai_paddle)
if paddle_center < ball.y:
    ai_paddle.move_down(HEIGHT)
elif paddle_center > ball.y:
    ai_paddle.move_up()
```

---

### Line 149: Ball Radius Multiplication
```python
pygame.draw.rect(screen, WHITE, (ball.x - ball.radius, ball.y - ball.radius, 
                                  ball.radius * 2, ball.radius * 2))
```
**Issue:** `ball.radius * 2` computed to get diameter (magic calculation)
**Severity:** MEDIUM
**Fix:**
```python
def get_ball_diameter(ball):
    """Get ball diameter for drawing."""
    return ball.radius * 2

# Or add property to Ball class:
@property
def diameter(self):
    return self.radius * 2
```

---

### Lines 55-56: Font Hardcoding
```python
font = pygame.font.Font(None, size)
img = font.render(text, True, WHITE)
```
**Issue:** `None` (system font) and `True` (antialias) are magic values
**Severity:** LOW
**Fix:**
```python
SYSTEM_FONT = None
FONT_ANTIALIAS = True

def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(SYSTEM_FONT, size)
    img = font.render(text, FONT_ANTIALIAS, WHITE)
    screen.blit(img, (x, y))
```

---

### Lines 152-155: Position Magic Numbers
```python
pygame.draw.line(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 1)
draw_text(screen, str(player_score), 64, WIDTH / 4, 20)
draw_text(screen, str(ai_score), 64, WIDTH * 3 / 4, 20)
```
**Severity:** MEDIUM (3 magic numbers)
**Fix:**
```python
# Constants at module level
SCORE_POSITION_LEFT_X_RATIO = 0.25
SCORE_POSITION_RIGHT_X_RATIO = 0.75
SCORE_TEXT_TOP_Y = 20
SCORE_TEXT_SIZE = 64
CENTER_LINE_WIDTH = 1

# In render function:
center_x = WIDTH / 2
pygame.draw.line(screen, WHITE, (center_x, 0), (center_x, HEIGHT), CENTER_LINE_WIDTH)
draw_text(screen, str(player_score), SCORE_TEXT_SIZE, 
          int(WIDTH * SCORE_POSITION_LEFT_X_RATIO), SCORE_TEXT_TOP_Y)
draw_text(screen, str(ai_score), SCORE_TEXT_SIZE,
          int(WIDTH * SCORE_POSITION_RIGHT_X_RATIO), SCORE_TEXT_TOP_Y)
```

---

## Documentation Issues

### Missing Docstrings

| Location | Type | Missing Doc |
|----------|------|------------|
| Line 1 | Module | Yes - add module docstring |
| Line 12 | Class: Ball | Yes |
| Line 13 | Method: Ball.__init__ | Yes |
| Line 21 | Method: Ball.move | Yes |
| Line 29 | Method: Ball.reset | Yes |
| Line 35 | Class: Paddle | Yes |
| Line 36 | Method: Paddle.__init__ | Yes |
| Line 49 | Method: Paddle.move_down | Yes |
| Line 54 | Function: draw_text | Yes |
| Line 59 | Function: init_game | Yes |
| Line 85 | Function: handle_collisions | Yes |
| Line 117 | Function: game_loop | Yes |
| Line 160 | Function: main | Yes |

**Only 2 have docstrings:** `move_up()` (line 43-44)

---

## PEP 8 Violations - Line Length

| Line | Length | Content | Fix |
|------|--------|---------|-----|
| 72 | 104 | `player_paddle = Paddle(0, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)` | Break into multiple lines |
| 73 | 119 | `ai_paddle = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)` | Break into multiple lines |
| 144 | 109 | `player_score_change, ai_score_change = handle_collisions(ball, player_paddle, ai_paddle, game_config)` | Use intermediate variable or multiline |
| 149 | 119 | `pygame.draw.rect(screen, WHITE, (ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2))` | Create Rect object or use helper |
| 150 | 118 | `pygame.draw.rect(screen, WHITE, (player_paddle.x, player_paddle.y, player_paddle.width, player_paddle.height))` | Create Rect objects |
| 151 | 102 | `pygame.draw.rect(screen, WHITE, (ai_paddle.x, ai_paddle.y, ai_paddle.width, ai_paddle.height))` | Create Rect objects |
| 164 | 82 | `ball, player_paddle, ai_paddle, screen, clock, game_config = init_game(config)` | Acceptable, just over by 3 chars |

---

## Code Duplication Analysis

### Duplication 1: Paddle Initialization (Lines 72-73)
**Similarity:** ~80%
```python
player_paddle = Paddle(0, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
ai_paddle = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
```

**Better approach:**
```python
def create_paddles(width, height, paddle_width, paddle_height, paddle_speed):
    """Create player and AI paddles."""
    center_y = height / 2 - paddle_height / 2
    player = Paddle(0, center_y, paddle_width, paddle_height, paddle_speed)
    ai = Paddle(width - paddle_width, center_y, paddle_width, paddle_height, paddle_speed)
    return player, ai
```

---

### Duplication 2: Config Unpacking
**Severity:** MEDIUM - repeated in 3 functions

**Functions affected:**
- `init_game()` lines 60-65
- `handle_collisions()` lines 86-89  
- `game_loop()` lines 121-123

**Total:** 12 lines of nearly identical dictionary unpacking

**Better approach:** Use dataclass
```python
from dataclasses import dataclass

@dataclass
class GameConfig:
    window_width: int
    window_height: int
    ball_size: int
    paddle_width: int
    paddle_height: int
    ball_speed: int
    paddle_speed: int

# No more unpacking needed!
```

---

## Summary Table: Issues by Line

| Line(s) | Issue | Type | Severity |
|---------|-------|------|----------|
| 6 | pygame.init() at module level | Anti-pattern | MEDIUM |
| 26, 46, 51 | Boundary magic numbers | Magic Number | MEDIUM |
| 55, 56 | Font hardcoding | Magic Value | LOW |
| 60-65 | Config unpacking without validation | Both | HIGH |
| 71-73 | Paddle initialization with magic numbers | Both | HIGH |
| 72-73 | PEP 8 line length | Style | MEDIUM |
| 85-115 | handle_collisions complexity + duplication | CC + DRY | MEDIUM |
| 102, 113 | Ball reset duplication | Duplication | MEDIUM |
| 117-158 | game_loop complexity + responsibilities | CC | MEDIUM |
| 144 | PEP 8 line length | Style | MEDIUM |
| 149-151 | pygame.draw.rect duplication + PEP 8 | Both | MEDIUM |
| 152 | CENTER_LINE magic number | Magic | MEDIUM |
| 154-155 | Score position magic numbers | Magic | MEDIUM |
| 161-162 | Missing error handling | Error Handling | HIGH |
| 164 | Return statement + PEP 8 | Style | LOW |

