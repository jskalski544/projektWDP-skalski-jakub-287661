import pygame
import sys
import time
import random


class Box:
    def __init__(self, color, shape, is_revealed):
        self.color = color
        self.shape = shape
        self.is_revealed = is_revealed


FPS = 30
WINDOWHEIGHT = 660
WINDOWWIDTH = 1280
REVEALSPEED = 8
BOXSIZE = 80
GAPSIZE = 20
COLUMNS = 6
ROWS = 5
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

assert (COLUMNS * ROWS) % 2 == 0


# colors_list
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 51, 153)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (102, 0, 102)
DARKBLUE = (25, 0, 51)
WHITE = (255, 255, 255)

BGCOLOR = DARKBLUE
BOXCOLOR = WHITE

# shapes_list(z internetu)
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, BLUE, GREEN, PINK, YELLOW, ORANGE, PURPLE)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert (COLUMNS * ROWS) <= len(ALLCOLORS) * len(ALLSHAPES)

board = []
_mouse_pos = (0, 0)
last_revealed = []  # indexes of two lastly revealed boxes
start = 0


def main():
    pygame.display.set_caption("Memory game")
    generate_puzzles()
    draw_board()
    fpsclock = pygame.time.Clock()
    fpsclock.tick(FPS)
    while True:
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                global _mouse_pos
                global start
                if not start:
                    start = time.time()
                _mouse_pos = pygame.mouse.get_pos()
                draw_board()
                check_if_over()


def draw_icon(shape, color, left, top):
    """this function draws the shapes from ALLSHAPES list(z internetu)"""
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)
    if shape == DONUT:
        pygame.draw.circle(screen, color, (left + half, top + half), half - 5)
        pygame.draw.circle(screen, WHITE, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(screen, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(screen, color,
                            ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1),
                             (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(screen, color, (left, top + i), (left + i, top))
            pygame.draw.line(screen, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(screen, color, (left, top + quarter, BOXSIZE, half))


def draw_board():
    """this function draws the board and then flips the boxes that are clicked"""
    screen.fill(BGCOLOR)
    boxx = (WINDOWWIDTH - (BOXSIZE * COLUMNS + GAPSIZE * (COLUMNS - 1))) // 2
    boxy = (WINDOWHEIGHT - (BOXSIZE * ROWS + GAPSIZE * (ROWS - 1))) // 2
    for k in range(ROWS):
        for j in range(COLUMNS):
            box = board[k * COLUMNS + j]
            rect = pygame.draw.rect(screen, BOXCOLOR, pygame.Rect(boxx, boxy, BOXSIZE, BOXSIZE))
            if rect.collidepoint(_mouse_pos) and not box.is_revealed:
                box.is_revealed = True
                last_revealed.append(k * COLUMNS + j)
            if box.is_revealed:
                draw_icon(box.shape, box.color, boxx, boxy)
            boxx += GAPSIZE + BOXSIZE
        boxy += GAPSIZE + BOXSIZE
        boxx = (WINDOWWIDTH - (BOXSIZE * COLUMNS + GAPSIZE * (COLUMNS - 1))) // 2
    pygame.display.flip()
    if len(last_revealed) == 2:
        check_if_pair()


def check_if_pair():
    """this function checks if the boxes that were last revealed are matching"""
    global last_revealed
    global _mouse_pos
    _mouse_pos = (0, 0)
    box1 = board[last_revealed[0]]
    box2 = board[last_revealed[1]]
    if box1.color != box2.color or box1.shape != box2.shape:
        pygame.time.wait(500)
        board[last_revealed[0]].is_revealed = False
        board[last_revealed[1]].is_revealed = False
        last_revealed = []
        draw_board()
    else:
        last_revealed = []


def generate_puzzles():
    """this function creates all the combinations to pair up shapes and colors
     in order to generate all the puzzles possible"""
    colorsnum = len(ALLCOLORS)
    shapesnum = len(ALLSHAPES)
    boxesnum = COLUMNS * ROWS
    puzzles = []
    for k in range(colorsnum):
        for j in range(shapesnum):
            puzzles.append((ALLCOLORS[k], ALLSHAPES[j]))
    random.shuffle(puzzles)
    for i in range(boxesnum // 2):
        board.append(Box(puzzles[i][0], puzzles[i][1], False))
        board.append(Box(puzzles[i][0], puzzles[i][1], False))
    random.shuffle(board)


def check_if_over():
    """this function checks if the game is finished by a player"""
    for k in range(len(board)):
        if not board[k].is_revealed:
            return False
    pygame.font.init()
    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 30)
    text = font.render("You won, it took you " + str(round(time.time() - start, 2)) + " seconds", True, WHITE, BGCOLOR)
    text_rect = text.get_rect()
    text_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    screen.blit(text, text_rect)
    pygame.mixer.init()
    pygame.mixer.music.load('Danza.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(0, 8, 0)
    pygame.display.update()
    return True


if __name__ == '__main__':
    main()
