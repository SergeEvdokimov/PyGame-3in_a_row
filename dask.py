import pygame
import os
from random import randint
from main import load_image


class Board:
    def __init__(self, width, height, left=0, top=50):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.all_sprites = pygame.sprite.Group()
        self.left = left
        self.top = top
        self.cell_size = 420 // width

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = randint(1, 5)
                sprite = pygame.sprite.Sprite(self.all_sprites)
                sprite.image = load_image(f"{self.board[i][j]}.png", 'white')
                sprite.image = pygame.transform.scale(sprite.image, (self.cell_size, self.cell_size))
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = i * self.cell_size + self.left
                sprite.rect.y = j * self.cell_size + self.top
        self.all_sprites.draw(screen)


    def move(self, cell):
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

def game(lvl=7):
    pygame.init()
    size = 420, 470
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('3 в ряд')
    board = Board(lvl, lvl)
    screen.fill('white')
    cnt = 0
    cnt_fon = pygame.font.Font(None, 36)
    score = cnt_fon.render('Scores:', True, (255, 66, 103))
    counter = cnt_fon.render(f'{cnt}', True, (180, 0, 0))
    screen.blit(score, (10, 10))
    screen.blit(counter, (100, 10))
    board.render(screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.move(event.pos)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    levels = [7, 10, 12]
    lvl_num = randint(0, 2)
    game(levels[lvl_num])