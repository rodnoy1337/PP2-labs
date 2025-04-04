import pygame
import random
import time
import sys
import os

pygame.init()

# defining color tuples
BLACK = (0, 0, 0)
WHITE = (50, 50, 50)

# defining sizes of the screen and single block
HEIGHT = 400
WIDTH = 400
CELL_SIZE = 20

# defining font and text
font = pygame.font.SysFont("impact", 20)
over = font.render("GAME OVER", True, BLACK)
title = font.render("Snake", True, BLACK)
title2 = font.render("Press 'Enter' to start the game", True, BLACK)
final1 = font.render("Congratulation!", True, BLACK)
final2 = font.render("You've reached the end of the game!", True, BLACK)

# setting the global variables
score = 0
last_score = 0
level = 1


class Point:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

# class for food sprite


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill((252, 186, 3))
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, 19) * CELL_SIZE,
                             random.randint(0, 19) * CELL_SIZE)

# class for a single block sprite of the wall


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill((3, 177, 252))
        self.level = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)

# class for the snake's head sprite


class Snake_head(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill((255, 0, 0))
        self.x = 10
        self.y = 15
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * CELL_SIZE, self.y * CELL_SIZE)
        self.dx = 0
        self.dy = 0

    # method for moving the head
    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x * CELL_SIZE >= WIDTH:
            self.x = 0
        if self.y * CELL_SIZE >= HEIGHT:
            self.y = 0
        if self.x < 0:
            self.x = WIDTH / CELL_SIZE
        if self.y < 0:
            self.y = HEIGHT / CELL_SIZE
        self.rect.topleft = (self.x * CELL_SIZE, self.y * CELL_SIZE)

# class for the snake's body


class Snake_body(pygame.sprite.Sprite):
    def __init__(self, front):  # receiving the parameters of the front block before the current block
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = front.rect.topleft

    # method of the moving snake's body
    def move(self, front):
        self.rect.topleft = front.rect.topleft

# function for showing the game's menu


def show_go_screen():
    SCREEN.fill(BLACK)
    box = pygame.Surface((400, 300))
    box.fill((255, 255, 255))
    box.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    box.blit(title2, (WIDTH//2 - title2.get_width()//2, 180))
    box.blit(font.render(
        f"Your last score is: {score}", True, BLACK), (125, 220))
    SCREEN.blit(box, (0, 50))
    pygame.display.update()
    waiting = True
    while waiting:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # starts the game when Enter/Return is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# function for resetting the game, variables for it and sprite groups


def init():
    global gameover, snake_list, score, level, food, all_sprites, head, food_sprite, walls, snake, head_sprite, newlevel, final_stage, body_sprite
    gameover, newlevel, final_stage = False, False, False
    head = Snake_head()
    snake_list = [head]
    map = []
    food = Food()

    all_sprites = pygame.sprite.Group()  # group for all sprites for drawing
    head_sprite = pygame.sprite.Group()  # group for the snake's head sprite
    body_sprite = pygame.sprite.Group()  # group for the body sections sprites
    food_sprite = pygame.sprite.Group()  # group for the food's sprite
    walls = pygame.sprite.Group()  # group for all the blocks of walls
    file = open(f'levels/level{level}.txt')  # loads the current level's file
    for y in range(0, 21):
        for x in range(0, 21):
            ch = file.read(1)
            if ch == '#':  # reading the coordinates of the each wall block and adding to the list of all wall blocks
                map.append(Wall(x, y))
            if ch == "@":  # reading the coordinates of the snake's head
                head.x = x
                head.y = y
                head.rect.topleft = (head.x * CELL_SIZE, head.y * CELL_SIZE)
    all_sprites.add(head, food, *map)
    head_sprite.add(head)
    food_sprite.add(food)
    walls.add(*map)

# main function


def main():
    global SCREEN, CLOCK, gameover, snake_list, score, last_score, level, food, all_sprites, head, food_sprite, walls, snake, newlevel, final_stage, body_sprite
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    speed = 0
    init()

    while True:

        if gameover == True or final_stage == True:  # checks flags of gameover or if user finished last map
            show_go_screen()  # triggers menu sreen
            level = 1  # resets the level, speed and score
            score = 0
            last_score = 0
            speed = 0
            init()

        if newlevel == True:  # checks the flag if user has reached new level
            init()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:  # changes the direction of head's movement depending on the key pressed
                if event.key == pygame.K_RIGHT:
                    head.dx = 1
                    head.dy = 0
                if event.key == pygame.K_LEFT:
                    head.dx = -1
                    head.dy = 0
                if event.key == pygame.K_UP:
                    head.dx = 0
                    head.dy = -1
                if event.key == pygame.K_DOWN:
                    head.dx = 0
                    head.dy = 1

        # changes randomly position of the food while it's colliding with walls or snake
        while pygame.sprite.spritecollide(food, walls, False) or pygame.sprite.spritecollide(food, body_sprite, False):
            food.rect.topleft = (random.randint(0, 19) *
                                 CELL_SIZE, random.randint(0, 19) * CELL_SIZE)

        # coliision check for snake's head and food
        if pygame.sprite.spritecollideany(head, food_sprite):
            # creates new body section with passed parameeters of the last block in snake's body
            b = Snake_body(snake_list[-1])
            all_sprites.add(b)
            body_sprite.add(b)
            snake_list.append(b)
            food.rect.topleft = (random.randint(0, 19) *
                                 CELL_SIZE, random.randint(0, 19) * CELL_SIZE)
            score += 1

        # new level for every n points, where n is the numnber of points that's needed to collect before levelup
        if score - last_score >= 3 and score != last_score:
            newlevel = True
            last_score = score
            level += 1
            speed += 2
            # checks if the level reached maximum
            if level > len(os.listdir('./levels')):
                final_stage = True
                t = pygame.Surface((400, 200))
                t.fill((255, 255, 255))
                t.blit(final1, (t.get_width()//2 - final1.get_width() //
                       2, t.get_height()//2 - final1.get_height()//2))
                t.blit(final2, (t.get_width()//2 - final2.get_width() //
                       2, t.get_height()//2 + 30 - final2.get_height()//2))
                SCREEN.blit(t, (0, 100))
                pygame.display.flip()
                time.sleep(2)

            for entity in all_sprites:  # removing all sprites
                entity.kill()

        for i in range(len(snake_list) - 1, 0, -1):  # moving snake's body
            snake_list[i].move(snake_list[i - 1])
        head.move()  # moving snake's head

        # collision check for snake's head and any of the wall blocks
        if pygame.sprite.spritecollideany(head, walls) or pygame.sprite.spritecollideany(head, body_sprite):
            gameover = True  # sets the flag for gameover
            rect = pygame.Surface((200, 200))
            rect.fill((255, 255, 255))
            rect.blit(over, (rect.get_width()//2 - over.get_width() //
                      2, rect.get_height()//2 - over.get_height()//2))
            SCREEN.blit(rect, (100, 100))
            pygame.display.flip()
            for entity in all_sprites:  # removing all sprites
                entity.kill()
            time.sleep(2)
        SCREEN.fill(BLACK)

        for sprite in all_sprites:  # drawing all sprites on the map
            SCREEN.blit(sprite.image, sprite.rect)
        drawGrid()

        score_counter = font.render(f"Score: {score}", True, (214, 75, 32))
        level_counter = font.render(f"Level: {level}", True, (214, 75, 32))
        SCREEN.blit(score_counter, (5, 5))
        SCREEN.blit(level_counter, (5, 30))

        pygame.display.update()

        CLOCK.tick(5 + speed)


def drawGrid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


main()
