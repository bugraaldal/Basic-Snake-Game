import sys
import time
import random
from pygame.math import Vector2
import pygame as pg

#t0 = time.process_time()

# Creating a path and a text file to keep track of the best score 
cur_path = os.getcwd()
if not(os.path.isdir(f"{cur_path}/snake_game/")):
    os.mkdir(f"{cur_path}/snake_game/")
    os.chdir(f"{cur_path}/snake_game/")
    f = open(f"{os.getcwd()}/Best.txt", "w+").close()
    a = open(f"{os.getcwd()}/Best.txt", "r+")
    a.write("0")
    a.close()


class points:
    def __init__(self):
        # Calls the randomize function - __init__ to constantly do that
        self.randomize()

    def point(self):
        # Prints the point to the screen
        point = pg.Rect(self.xy.x*cellSize, self.xy.y *
                        cellSize, cellSize, cellSize)
        pg.draw.rect(screen, "red", point)  # (255, 213, 75)

    def randomize(self):
        # Randomizes the point coordinates
        self.x, self.y = random.randint(0, cells-1), random.randint(0, cells-1)
        self.xy = Vector2(self.x, self.y)


class _snake:
    def __init__(self):
        # Beggining coordinates of the sname
        self.snake = [Vector2(8, 12), Vector2(9, 12), Vector2(10, 12)]
        self.direct = Vector2(0, 0)
        self.big = False

    def snake_(self):
        # Draws the snake
        for block in self.snake:
            x = block.x * cellSize
            y = block.y * cellSize
            blockRec = pg.Rect(x, y, cellSize, cellSize)
            pg.draw.rect(screen, (255, 137, 47), blockRec)

    def snakeMovement(self):
        # The movement of the snake. Basically, the body is following the beginning point (head)
        if self.big == True:
            body = self.snake[:]
            body.insert(0, body[0]+self.direct)
            self.snake = body[:]
            self.big = False
        # If snake gets longer, appends a block
        else:
            body = self.snake[0:-1]
            body.insert(0, body[0]+self.direct)
            self.snake = body[:]

    def reset(self):
        # Resets the game when dead or pressed to space
        global cells
        self.snake = [Vector2(8, 12), Vector2(9, 12), Vector2(10, 12)]
        self.direct = Vector2(0, 0)
        cells = 20

    def grow(self):
        self.big = True


class main:
    def __init__(self):
        self.points = points()
        self._snake = _snake()

    def update(self):
        self._snake.snakeMovement()
        self.point_get()
        self.die()

    def draw_objs(self):
        # The things that are constintly happen/change
        self.texturedbg()
        self.points.point()
        self._snake.snake_()
        self.scoreShow()

    def point_get(self):
        # getting a point, if the coordinates of the head equals to the coordinates of the point, grow and get bigger
        global cells
        if self._snake.snake[0] == self.points.xy:
            self.points.randomize()
            self._snake.grow()
        for part in self._snake.snake[1:]:
            if part == self.points.xy:
                self.points.randomize()
#        if len(self._snake.snake) % 2 == 0:
#            t1 = time.process_time() - t0
#            if t1 > 5:
#                cells -= 1

    def die(self):
        # Resets the game if ypu hit your head to your body or to the walls
        if not 0 <= self._snake.snake[0].x < cells or not 0 <= self._snake.snake[0].y < cells:
            self.gameOver()
        for part in self._snake.snake[1:]:
            if part == self._snake.snake[0]:
                self.gameOver()

    def gameOver(self):
        self._snake.reset()

    def scoreShow(self):
        # Opens a file, reads it and shows it on the screen
        f = open(f"{os.getcwd()}/Best.txt", "r+")
        Stimes = int(f.read())
        snaketall = len(self._snake.snake) - 3
        if snaketall > Stimes:
            f.close()
            k = open(f"{os.getcwd()}/Best.txt", "w")
            k.write(str(snaketall))
            k.close()
            snaketall = Stimes
        f.close()
        bestText = f"Best: {str(Stimes)}"
        scoreText = f"Score: {str(snaketall)}"
        scoreSurf = scoreLabel.render(scoreText, False, "black")
        _x, _y = cellSize*cells-100, cellSize*cells-60
        scoreRec = scoreSurf.get_rect(center=(_x, _y))
        screen.blit(scoreSurf, scoreRec)
        BestSurf = scoreLabel.render(bestText, False, "black")
        x, y = cellSize*cells-100, cellSize*cells-120
        BestRec = BestSurf.get_rect(center=(x, y))
        screen.blit(BestSurf, BestRec)

    def texturedbg(self):
        # Configure the pointy background
        for row in range(cells):
            if row % 2 == 0:
                for coll in range(cells):
                    if coll % 2 == 0:
                        lGreen = pg.Rect(coll*cellSize, row *
                                         cellSize, cellSize, cellSize)
                        pg.draw.rect(screen, (138, 209, 91), lGreen)
            else:
                for coll in range(cells):
                    if coll % 2 != 0:
                        lGreen = pg.Rect(coll*cellSize, row *
                                         cellSize, cellSize, cellSize)
                        pg.draw.rect(screen, (138, 209, 91), lGreen)


# Basic configurations of the pygame
cells = 20
cellSize = 40
pg.init()
screenVar = pg.USEREVENT
pg.time.set_timer(screenVar, 150)
size = cellSize*cells
screen = pg.display.set_mode((size, size))
gameOn = True
clock = pg.time.Clock()
scoreLabel = pg.font.SysFont(None, 50)

mainGame = main()
while gameOn:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == screenVar:
            mainGame.update()
        if event.type == pg.KEYDOWN:
            # Getting the pressed buttons
            if event.key == pg.K_UP and mainGame._snake.direct != Vector2(0, 1):
                mainGame._snake.direct = Vector2(0, -1)
            if event.key == pg.K_LEFT and mainGame._snake.direct != Vector2(1, 0):
                mainGame._snake.direct = Vector2(-1, 0)
            if event.key == pg.K_RIGHT and mainGame._snake.direct != Vector2(-1, 0):
                mainGame._snake.direct = Vector2(1, 0)
            if event.key == pg.K_DOWN and mainGame._snake.direct != Vector2(0, -1):
                mainGame._snake.direct = Vector2(0, 1)
            if event.key == pg.K_SPACE:
                mainGame._snake.reset()
    screen.fill(pg.Color((228, 255, 153)))
    mainGame.draw_objs()
    pg.display.update()
    clock.tick(60)
