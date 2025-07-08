from typing import *
import pygame
import sys
from settings import *
from score_manager import load_scores

def show_pause_menu(screen, font) -> Literal["continue", "menu", "exit"]:   # Меню паузы
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Заголовок
    pause_text = font.render("Пауза", True, (255, 255, 255))
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 200))   # Центрирование

    # Кнопки в меню паузы
    buttons: List[Tuple[str, str, Tuple[int, int, int], Tuple[int, int, int, int]]]  = [
        ("continue", "Продолжить", (100, 200, 100), (SCREEN_WIDTH // 2 - 100, 300, 200, 50)),
        ("menu", "В меню", (100, 150, 250), (SCREEN_WIDTH // 2 - 100, 370, 200, 50)),
        ("exit", "Выход", (200, 100, 100), (SCREEN_WIDTH // 2 - 100, 440, 200, 50))
    ]

    for btn_type, btn_text, btn_color, btn_rect in buttons:
        rect = pygame.Rect(*btn_rect)   # Преобразование к Rect
        pygame.draw.rect(screen, btn_color, rect, border_radius=12)   # Отрисовка кнопки
        text = font.render(btn_text, True, (0, 0, 0))   # Текст каждой кнопки
        screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    pygame.display.flip()

    # Действия при клике по кнопке/ закрытии окна
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn_type, _, _, btn_rect in buttons:
                    rect = pygame.Rect(*btn_rect)
                    if rect.collidepoint(mouse_pos):
                        return btn_type

def show_menu(screen, font, saved_game_exists: bool)-> Literal["continue", "start", "rules", "exit"]:   # Ukfdyjt vry.
    screen.fill((181, 204, 255))

    # Заголовок
    title_text = font.render("Соедини Точки", True, (0, 0, 0))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    buttons: List[Tuple[str, str, Tuple[int, int, int], Tuple[int, int, int, int]]] = []   # Список кнопок в меню
    y_pos = 120   # Позиция начальной кнопки

    if saved_game_exists:   # При сохранении добавляем кнопку продолжить
        buttons.append(("continue", "Продолжить", (100, 200, 100), (SCREEN_WIDTH // 2 - 100, y_pos, 200, 50)))
        y_pos += 70

    buttons.extend([   # добавляем остальные кнопки со смещением по y
        ("start", "Новая игра", (100, 150, 250), (SCREEN_WIDTH // 2 - 100, y_pos, 200, 50)),
        ("rules", "Правила", (100, 150, 250), (SCREEN_WIDTH // 2 - 100, y_pos + 70, 200, 50)),
        ("exit", "Выход", (200, 100, 100), (SCREEN_WIDTH // 2 - 100, y_pos + 140, 200, 50))
    ])

    for btn_type, btn_text, btn_color, btn_rect in buttons:
        rect = pygame.Rect(*btn_rect)   # Преобразование к Rect
        pygame.draw.rect(screen, btn_color, rect, border_radius=12)   # Отрисовка кнопки
        text = font.render(btn_text, True, (0, 0, 0))   # Текст каждой кнопки
        screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    scores_title = font.render("Таблица рекордов", True, (0, 0, 0))   # Таблица рекордов
    screen.blit(scores_title, (SCREEN_WIDTH // 2 - scores_title.get_width() // 2, y_pos + 220))   # Заголовок

    scores: List[int] = load_scores()   # Загрузка результатов из файла

    start_y: int = y_pos + 270
    line_height: int = 40
    for i in range(len(scores)):   # Отрисовка результатов со смещением
        rank: int = i + 1
        score_value: int = scores[i]
        text_str = f"{rank}. {score_value}"
        score_text = font.render(text_str, True, (0, 0, 0))
        pos_x: int = SCREEN_WIDTH // 2 - score_text.get_width() // 2
        pos_y: int = start_y + i * line_height
        screen.blit(score_text, (pos_x, pos_y))

    pygame.display.flip()

    # Действия при клике по кнопке/ закрытии окна
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn_type, _, _, btn_rect in buttons:
                    rect = pygame.Rect(*btn_rect)
                    if rect.collidepoint(mouse_pos):
                        return btn_type

def show_game_over(screen, font, score) -> Literal["restart", "menu"]:   # Экран при завершении
    screen.fill((181, 204, 255))

    # Заголовок
    game_over_text = font.render("Игра окончена! Ваш счет: " + str(score), True, (0, 0, 0))

    # Кнопки
    restart_text = font.render("Заново", True, (0, 0, 0))
    menu_text = font.render("В меню", True, (0, 0, 0))

    restart_button = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 50, 180, 50)
    menu_button = pygame.Rect(SCREEN_WIDTH//2 + 40, SCREEN_HEIGHT//2 + 50, 180, 50)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    pygame.draw.rect(screen, (100, 150, 250), restart_button, border_radius=12)
    pygame.draw.rect(screen, (100, 150, 250), menu_button, border_radius=12)

    screen.blit(restart_text, (restart_button.centerx - restart_text.get_width()//2, restart_button.centery - restart_text.get_height()//2))
    screen.blit(menu_text, (menu_button.centerx - menu_text.get_width()//2, menu_button.centery - menu_text.get_height()//2))

    pygame.display.flip()

    # Действия при клике по кнопке/ закрытии окна
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(pos):
                    return "restart"
                elif menu_button.collidepoint(pos):
                    return "menu"


def show_rules(screen, font) -> None:
    screen.fill((181, 204, 255))

    # Заголовок
    title_text = font.render("Правила игры", True, (0, 0, 0))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    # Текст правил
    rules: List[str] = [
        "Как играть:",
        "1. Соединяйте точки одного цвета",
        "2. Можно соединять только соседние точки",
        "3. Минимальная длина цепочки - 2 точки",
        "4. У вас есть 20 ходов",
        "5. Очки считаются по формуле: N*(N-1),",
        "   где N - количество точек в цепочке",
        "",
        "Цель: набрать как можно больше очков!"
    ]

    y_pos = 120
    line_height = 40
    for line in rules:
        if line:  # Пропускаем пустые строки
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (50, y_pos))
        y_pos += line_height

    # Кнопка назад
    back_text = font.render("Назад", True, (0, 0, 0))
    back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, (100, 150, 250), back_button, border_radius=12)
    screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - back_text.get_height() // 2))

    pygame.display.flip()

    # Действия при клике по кнопке/ закрытии окна
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return