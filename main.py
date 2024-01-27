import pygame
from load_image import load_image
from dask import Board
import sys
from PyQt5.QtWidgets import QApplication
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

con = sqlite3.connect('Results.sqlite')
cur = con.cursor()
size = (700, 700)
nickname = ''

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
        if not company_is_registered:
            cur.execute(f"""INSERT INTO result(Name, num_of_move) 
                                    VALUES('{nickname}', '{0}')""")
            con.commit()
        self.close()


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
    cnt = 0
    if line_for_del is not None:
        cnt = len(line_for_del)
    while line_for_del is not None:
        board.delete(line_for_del)
        line_for_del = board.del_line()
    return cnt


def main():
    app = QApplication(sys.argv)
    ex = Enter()
    #sys.exit(app.exec_())

    global size
    pygame.init()
    screen = pygame.display.set_mode(size)
    start_background = pygame.sprite.Sprite()
    start_background_image = pygame.transform.scale(load_image("start_game.jpg"), size)
    start_background.image = start_background_image
    start_background.rect = start_background.image.get_rect()
    pygame.display.set_caption('3 в ряд')

    ex.show()

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
                new_board = make_current_board(board)
                if new_board:  # если очки прибавились, то обновляем счетчик
                    cnt += new_board
                    step_cnt += 1
                    pygame.draw.rect(screen2, 'white', (100, 10, 100, 25))
                    counter = cnt_fon.render(f'{cnt}', True, (180, 0, 0))
                    screen2.blit(counter, (100, 10))
        pygame.display.flip()
    cur.execute(f'''UPDATE result SET num_of_move = "{step_cnt}"
                        WHERE Name = "{nickname}"''')
    con.commit()
    #  TODO: таблица результатов
    pygame.quit()


if __name__ == '__main__':
    main()
