import pygame
import os
import sys
from random import randint

size = (700, 700)


class Board:
    def __init__(self, side, left=0, top=50):
        self.side = side
        self.board = [[randint(1, 5) for _ in range(side)] for _ in range(side)]
        self.all_sprites = pygame.sprite.Group()
        self.left = left
        self.top = top
        self.cell_size = 420 // side

    def render(self, screen):
        squares = []
        for i in range(self.side):
            for j in range(self.side):
                sprite = pygame.sprite.Sprite(self.all_sprites)
                sprite.image = load_image(f"{self.board[i][j]}.png", 'white')
                sprite.image = pygame.transform.scale(sprite.image, (self.cell_size, self.cell_size))
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = i * self.cell_size + self.left
                sprite.rect.y = j * self.cell_size + self.top
                squares.append((sprite.rect.x, sprite.rect.y, self.cell_size, self.cell_size))
        self.all_sprites.draw(screen)
        for square in squares:
            pygame.draw.rect(screen, 'black', square, 1)

    def move(self, cell):
        pass

    def on_click(self, cell):
        pass

    def get_cell(self, mouse_pos):
        cell_x, cell_y = (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= cell_x <= self.side and 0 <= cell_y <= self.side:
            return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def del_line(self):
        line_to_del = []
        for x in range(1, self.side - 1):
            for y in range(1, self.side - 1):
                if self.board[x - 1][y] == self.board[x][y] == self.board[x + 1][y]:
                    line_to_del.extend([(x - 1, y), (x, y), (x + 1, y)])
                    for x_add in range(x - 1, 0, -1):
                        if self.board[x_add][y] == line_to_del[0]:
                            line_to_del.append((x_add, y))
                    for x_add in range(x + 1, self.side):
                        if self.board[x_add][y] == line_to_del[0]:
                            line_to_del.append((x_add, y))
                if self.board[x][y - 1] == self.board[x][y] == self.board[x][y + 1]:
                    line_to_del.extend([(x, y - 1), (x, y), (x, y + 1)])
                    for y_add in range(y - 1, 0, -1):
                        if self.board[x][y_add] == line_to_del[0]:
                            line_to_del.append((x, y_add))
                    for y_add in range(y + 1, self.side):
                        if self.board[x][y_add] == line_to_del[0]:
                            line_to_del.append((x, y_add))
        if line_to_del:
            return line_to_del
        return


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def intro(screen, start_background_image):
    intro_text = ["Выберить размер поля:", "7 на 7", "10 на 10", "12 на 12"]
    fon = pygame.transform.scale(start_background_image, size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_y = 400
    levels = []

    for line in intro_text:
        text = font.render(line, 1, 'white')
        rect = text.get_rect()
        text_y += 30
        rect.topleft = (30, text_y)
        text_y += rect.height
        screen.blit(text, rect)
        levels.append([rect.x, rect.y, rect.width, rect.height])

    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                for i in levels:
                    if i[0] <= x <= i[0] + i[2] and i[1] <= y <= i[1] + i[3]:
                        return levels.index(i)
        pygame.display.flip()


def main():
    global size
    pygame.init()
    screen = pygame.display.set_mode(size)
    start_background = pygame.sprite.Sprite()
    start_background_image = pygame.transform.scale(load_image("start_game.jpg"), size)
    start_background.image = start_background_image
    start_background.rect = start_background.image.get_rect()
    pygame.display.set_caption('3 в ряд')

    lvl_num = intro(screen, start_background_image)
    size = 420, 470
    screen2 = pygame.display.set_mode(size)
    pygame.display.set_caption('3 в ряд')
    if lvl_num == 1:
        board = Board(7)
    elif lvl_num == 2:
        board = Board(10)
    else:
        board = Board(12)
    screen2.fill('white')
    cnt = 0
    cnt_fon = pygame.font.Font(None, 36)
    score = cnt_fon.render('Scores:', True, (255, 66, 103))
    counter = cnt_fon.render(f'{cnt}', True, (180, 0, 0))
    screen2.blit(score, (10, 10))
    screen2.blit(counter, (100, 10))
    board.render(screen2)
    pygame.display.flip()
    running = True
    print(board.del_line())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.move(event.pos)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
