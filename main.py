import pygame
import os
import sys

width, height = 700, 700


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
    fon = pygame.transform.scale(start_background_image, (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_y = 50
    levels = []

    for line in intro_text:
        text = font.render(line, 1, 'white')
        rect = text.get_rect()
        text_y += 30
        rect.topleft = (10, text_y)
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
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    start_background = pygame.sprite.Sprite()
    start_background_image = pygame.transform.scale(load_image("start_game.jpg"), (width, height))
    start_background.image = start_background_image
    start_background.rect = start_background.image.get_rect()
    pygame.display.set_caption('3 в ряд')

    lvl_num = intro(screen, start_background_image)
    print('Уровень номер', lvl_num)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('white')
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()