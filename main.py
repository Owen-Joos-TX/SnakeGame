import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
window_x, window_y = 720, 480
game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Snake Game')

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# FPS controller
fps_controller = pygame.time.Clock()

# Score
score = 0

class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, (window_x // 10)) * 10
        self.rect.y = random.randrange(1, (window_y // 10)) * 10

class Snake(pygame.sprite.Group):
    def __init__(self):
        self.blocks = [SnakeBlock(100, 50), SnakeBlock(90, 50), SnakeBlock(80, 50)]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def draw(self, surface):
      for block in self.blocks:
            surface.blit(block.image, block.rect)

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != 'DOWN':
                self.change_to = 'UP'
            elif event.key == pygame.K_DOWN and self.direction != 'UP':
                self.change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                self.change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                self.change_to = 'RIGHT'
    
    def move(self):
        if self.change_to == 'UP':
            new_head_pos = (self.blocks[0].rect.x, self.blocks[0].rect.y - 10)
        elif self.change_to == 'DOWN':
            new_head_pos = (self.blocks[0].rect.x, self.blocks[0].rect.y + 10)
        elif self.change_to == 'LEFT':
            new_head_pos = (self.blocks[0].rect.x - 10, self.blocks[0].rect.y)
        elif self.change_to == 'RIGHT':
            new_head_pos = (self.blocks[0].rect.x + 10, self.blocks[0].rect.y)
        
        # Insert new block as the head
        new_head = SnakeBlock(new_head_pos[0], new_head_pos[1])
        self.blocks.insert(0, new_head)
        
        # Remove the tail block
        tail = self.blocks.pop()
        
        # Update direction
        self.direction = self.change_to

        # Check for collisions with boundaries (for game over conditions)
        if self.blocks[0].rect.x < 0 or self.blocks[0].rect.x >= window_x or self.blocks[0].rect.y < 0 or self.blocks[0].rect.y >= window_y:
            game_over()


def check_collision(snake, apple):
    if snake.blocks[0].rect.colliderect(apple.rect):
        return True
    return False

def game_over():
    pygame.quit()
    sys.exit()

snake = Snake()
apple = Apple()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        snake.update(event)
    
    snake.move()
    game_window.fill(black)
    
    if check_collision(snake, apple):
        score += 1
        apple.kill()
        # Extend the snake
        snake.blocks.append(SnakeBlock(snake.blocks[-1].rect.x, snake.blocks[-1].rect.y))
