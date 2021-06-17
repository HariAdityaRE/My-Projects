import pygame
import sys
import os
import numpy as np

width = 650
height = 650
screen = pygame.display.set_mode((width, height))
player = 1
bg_color = (51, 255, 196)
line_color = (0, 0, 0)
o_color = (255, 255, 255)
board = np.zeros((3, 3))
game_over = False
box_size = width // 3


def mark_square(row, col, player_no):
    board[row][col] = player_no
    if player_no == 1:
        pygame.draw.circle(screen, o_color, (col * box_size + (box_size // 2), row * box_size + (box_size // 2)), 60,
                           15)
    else:
        x = box_size // 4
        y = box_size - x
        pygame.draw.line(screen, line_color, (col * box_size + x, row * box_size + y),
                         (col * box_size + y, row * box_size + x), 15)
        pygame.draw.line(screen, line_color, (col * box_size + x, row * box_size + x),
                         (col * box_size + y, row * box_size + y), 15)


def available(row, col):
    return board[row][col] == 0


def check_win():
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            pygame.draw.line(screen, line_color, (15, i * box_size + 100), (width - 25, i * box_size + 100), 15)
            return True
    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            pygame.draw.line(screen, line_color, (i * box_size + 100, 15), (i * box_size + 100, height - 25), 15)
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        pygame.draw.line(screen, line_color, (15, 15), (width - 25, height - 25), 15)
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        pygame.draw.line(screen, line_color, (15, height - 25), (width - 25, 15), 15)
        return True
    return False


def is_full():
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return False
    return True


def draw_lines():
    x = box_size * 2
    pygame.draw.line(screen, line_color, (0, box_size), (width, box_size), 15)
    pygame.draw.line(screen, line_color, (0, x), (width, x), 15)
    pygame.draw.line(screen, line_color, (box_size, 0), (box_size, height), 15)
    pygame.draw.line(screen, line_color, (x, 0), (x, height), 15)


def show_result(z=0):
    print(pygame.font.get_fonts())
    text_font = pygame.font.SysFont('arialblack', 30)
    x, y = (width // 2 - box_size + 50), height // 2
    if not z:
        if player == 1:
            winner = 'O'
        else:
            winner = 'X'
        winner += " Has Won the Game"
    else:
        winner = "Its a Draw"
        x += 70
    text_to_display = text_font.render(winner, True, (255, 0, 0))
    screen.blit(text_to_display, (x, y))


def start():
    global player, screen, game_over, board, width, height, box_size
    game_over = False
    player = 1
    pygame.init()
    screen.fill(bg_color)
    board = np.zeros((3, 3))
    pygame.display.set_caption('TIC TAC TOE')
    draw_lines()
    while True:
        for event in pygame.event.get():
            if game_over or event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                pygame.time.wait(500)
                start()
            elif event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                clicked_row = mouse_y // box_size
                clicked_col = mouse_x // box_size
                if available(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win():
                        game_over = True
                        show_result()
                        continue
                    if board.all():
                        game_over = True
                        show_result(1)
                    player = player % 2 + 1
        pygame.display.update()


start()
