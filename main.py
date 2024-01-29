import pygame
import random
import sys
import sqlite3

from load_image import load_image
from dask import Board

from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

con = sqlite3.connect('Results.sqlite')
cur = con.cursor()
size = (700, 700)
nickname = ''


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, sprite_group, pos, dx, dy, width, height):
        super().__init__(sprite_group)
        self.screen_rect = (0, 0, width, height)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(self.screen_rect):
            self.kill()


class Enter(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Enter.ui', self)
        self.setWindowTitle("Вход")
        self.EnterButton.clicked.connect(self.enter)

    # Вход
    def check_name(self, name):
        return len(cur.execute(f"""SELECT * FROM result
                        WHERE Name = '{name}'""").fetchall())

    def enter(self):
        global nickname
        nickname = self.Name.text()
        company_is_registered = self.check_name(nickname)
        if nickname:
            if not company_is_registered:
                cur.execute(f"""INSERT INTO result(Name, num_of_move) 
                                        VALUES('{nickname}', '{0}')""")
                con.commit()
            self.close()
            game()
        else:
            self.statusBar().showMessage('Введите ник')


def intro(screen, start_background_image):
    intro_text = ["Выберите размер поля:", "7 на 7", "10 на 10", "12 на 12"]
    fon = pygame.transform.scale(start_background_image, size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_y = 400
    levels = []

    for line in intro_text:
        text = font.render(line, 1, (255, 66, 103))
        rect = text.get_rect()
        text_x = 240
        if line == "7 на 7":
            text_x = 320
        elif line != "Выберите размер поля:":
            text_x = 310
        text_y += rect.height
        rect.topleft = (text_x, text_y)
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


def make_current_board(board):
    line_for_del = board.del_line()
    deleted_line = line_for_del
    cnt = 0
    if line_for_del is not None:
        cnt = len(line_for_del)
    while line_for_del is not None:
        board.delete(line_for_del)
        line_for_del = board.del_line()
        deleted_line = deleted_line.union(line_for_del) if line_for_del is not None else deleted_line
    return cnt, deleted_line


def main():
    app = QApplication(sys.argv)
    ex = Enter()
    ex.show()
    sys.exit(app.exec())


def game():
    global size
    pygame.init()
    screen = pygame.display.set_mode(size)
    start_background = pygame.sprite.Sprite()
    star_animation = pygame.sprite.Group()
    clock = pygame.time.Clock()
    start_background_image = pygame.transform.scale(load_image("start_game.jpg"), size)
    start_background.image = start_background_image
    start_background.rect = start_background.image.get_rect()
    pygame.display.set_caption('3 в ряд')

    lvl_num = intro(screen, start_background_image)
    size = 420, 470
    screen2 = pygame.display.set_mode(size)
    pygame.display.set_caption('3 в ряд')
    if lvl_num == 1:
        board = Board(7, screen2)
    elif lvl_num == 2:
        board = Board(10, screen2)
    else:
        board = Board(12, screen2)
    screen2.fill('white')
    cnt, res = 0, 100
    step_cnt = 0
    cnt_fon = pygame.font.Font(None, 36)
    score = cnt_fon.render('Счет:', True, (255, 66, 103))
    need_score = cnt_fon.render('Цель: 100', True, (255, 66, 103))
    counter = cnt_fon.render(f'{cnt}', True, (180, 0, 0))
    screen2.blit(score, (10, 10))
    screen2.blit(counter, (100, 10))
    screen2.blit(need_score, (200, 10))
    board.render()
    pygame.display.flip()
    make_current_board(board)
    pygame.display.flip()
    running = True
    while running and cnt < res:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
                new_board, deleted_line = make_current_board(board)
                if new_board:  # если очки прибавились, то обновляем счетчик
                    numbers = range(-5, 6)
                    for x, y in deleted_line:
                        pos = [(x + 0.5) * board.cell_size + board.left, (y + 0.5) * board.cell_size + board.top]
                        for _ in range(10):
                            Particle(star_animation, pos, random.choice(numbers), random.choice(numbers), *size)
                    cnt += len(deleted_line)
                    step_cnt += 1
                    pygame.draw.rect(screen2, 'white', (100, 10, 100, 25))
                    counter = cnt_fon.render(f'{cnt}', True, (180, 0, 0))
                    screen2.blit(counter, (100, 10))
        board.render(screen=screen2, draw_only=True)
        star_animation.update()
        star_animation.draw(screen2)

        pygame.display.flip()
        clock.tick(100)
    cur.execute(f'''UPDATE result SET num_of_move = "{step_cnt}"
                            WHERE Name = "{nickname}"''')
    con.commit()
    #  TODO: таблица результатов
    pygame.quit()


if __name__ == '__main__':
    main()
