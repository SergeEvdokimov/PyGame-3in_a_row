import pygame
from random import randint
from load_image import load_image


class Board:
    def __init__(self, side, screen, left=0, top=50):
        self.screen = screen
        self.side = side
        self.board =[[randint(1, 5) for _ in range(side)] for _ in range(side)]
        self.all_sprites = pygame.sprite.Group()
        self.left = left
        self.top = top
        self.cell_size = 420 // side
        self.cells_for_swap = []

    def render(self, screen=None):
        if screen is None:
            screen = self.screen
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
        self.cells_for_swap.clear()

    # анимация
    def move(self, cell):
        pass

    # обмен клеток местами, после - перезаполнение
    def on_click(self):
        x1, y1 = self.cells_for_swap[0]
        x2, y2 = self.cells_for_swap[1]
        self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]
        self.render()
        pygame.display.flip()
        line_for_del = self.del_line()
        # в случае, если удалять нечего, клетки меняются обратно
        if line_for_del is None:
            pygame.time.delay(500)
            self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]
            self.render()

    # возвращает координаты клетки (ячейки в массиве)
    def get_cell(self, mouse_pos):
        cell_x, cell_y = (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= cell_x <= self.side and 0 <= cell_y <= self.side:
            return cell_x, cell_y

    # при нажатии на кнопку проверяется, было ли нажатие внутри поля
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.cells_for_swap.append(cell)
            if len(self.cells_for_swap) == 1:
                pygame.draw.rect(self.screen, 'green', (self.cells_for_swap[0][0] * self.cell_size + self.left,
                                                   self.cells_for_swap[0][1] * self.cell_size + self.top,
                                                   self.cell_size, self.cell_size), 1)
            elif len(self.cells_for_swap) == 2:
                if abs(cell[0] - self.cells_for_swap[0][0]) == 1 and cell[1] - self.cells_for_swap[0][1] == 0:
                    self.on_click()
                elif abs(cell[1] - self.cells_for_swap[0][1]) == 1 and cell[0] - self.cells_for_swap[0][0] == 0:
                    self.on_click()
                else:
                    self.render()

    # удаление клеток, возвращает координаты всех, которые следует удалить
    def del_line(self):
        line_to_del = []
        for x in range(self.side):
            for y in range(self.side):
                if 1 <= x < self.side - 1:
                    if self.board[x - 1][y] == self.board[x][y] == self.board[x + 1][y]:
                        line_to_del.extend([(x - 1, y), (x, y), (x + 1, y)])
                        for x_add in range(x - 1, 0, -1):
                            if self.board[x_add][y] == line_to_del[0]:
                                line_to_del.append((x_add, y))
                        for x_add in range(x + 1, self.side):
                            if self.board[x_add][y] == line_to_del[0]:
                                line_to_del.append((x_add, y))
                if 1 <= y < self.side - 1:
                    if self.board[x][y - 1] == self.board[x][y] == self.board[x][y + 1]:
                        line_to_del.extend([(x, y - 1), (x, y), (x, y + 1)])
                        for y_add in range(y - 1, 0, -1):
                            if self.board[x][y_add] == line_to_del[0]:
                                line_to_del.append((x, y_add))
                        for y_add in range(y + 1, self.side):
                            if self.board[x][y_add] == line_to_del[0]:
                                line_to_del.append((x, y_add))
        if line_to_del:
            # если вернется пустым, то удалять нечего
            return set(line_to_del)
        return

    # удаление и сдвиг
    def delete(self, line_for_del=[]):
        if len(line_for_del) == 0:
            return
        for cell in line_for_del:
            self.board[cell[0]][cell[1]] = 0
        for column in range(self.side):
            if 0 in self.board[column]:
                c = 0
                while (0 in self.board[column] and c < self.side):
                    # поднимает 0 вверх, после генерируя на их место новую картинку
                    for i in range(self.side - 1, c, -1):
                        if self.board[column][i] == 0:
                            self.board[column][i], self.board[column][i - 1] = self.board[column][i - 1], 0
                            if i - 1 == c:
                                self.board[column][i - 1] = randint(1, 5)
                        elif i - 1 == c and self.board[column][i - 1] == 0:
                            self.board[column][i - 1] = randint(1, 5);
                    c += 1
        self.render()