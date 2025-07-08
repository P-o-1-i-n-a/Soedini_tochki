import pygame
import sys
import random
from settings import *
from game import *
from ui import *
from typing import *
from score_manager import *
from save_manager import save_game, load_game, delete_save
from settings import SAVED_GAME

def main(saved_game: Optional[str] = None) -> None:
    global SAVED_GAME
    action: Optional[str] = None   # Действие из меню
    pygame.display.set_caption("Соедини точки")
    clock = pygame.time.Clock()

    is_paused: bool = False   # Флаг паузы

    dot_grid: List[List[Optional[Dict[str,Any]]]]
    score: int
    moves_left: int

    # Восстановление сохраненной игры
    if saved_game:
        dot_grid = saved_game['dot_grid']
        score = saved_game['score']
        moves_left = saved_game['moves_left']
    else:
        dot_grid = init_dot_grid()
        score = 0
        moves_left = 20

    current_path: List[Dict[str, Any]] = []   # Путь точек (соединенные)
    is_dragging: bool = False   # Флаг соединения
    current_color: Optional[Tuple[int, int, int]] = None   # Цвет соединения
    animating_phase: Literal["idle", "falling", "growing"] = "idle"   # Флаг анимации
    new_dots_to_add: List[Dict[str, Any]] = []   # Новые точки после падения

    # Кнопки интерфейса
    menu_text = font.render("В меню", True, (0, 0, 0))
    menu_button = pygame.Rect(SCREEN_WIDTH - 190, 16, 180, 50)
    pause_text = font.render("Пауза", True, (0, 0, 0))
    pause_button = pygame.Rect(SCREEN_WIDTH - 190, 80, 180, 50)

    # Цикл игры
    is_running: bool = True
    while is_running:
        screen.fill((181, 204, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Выход из игры
                save_game({
                    'dot_grid': dot_grid,
                    'score': score,
                    'moves_left': moves_left
                })
                is_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:   # Клик мыши
                mouse_pos: Tuple[int,int] = pygame.mouse.get_pos()

                if pause_button.collidepoint(mouse_pos):
                    is_paused = True
                    action = show_pause_menu(screen, font)   # Показать меню пацзы
                    if action == "continue":   # Кнопка продолжить
                        is_paused = False
                    elif action == "menu": # Сохраняем игру перед выходом в меню
                        SAVED_GAME = {
                            'dot_grid': dot_grid,
                            'score': score,
                            'moves_left': moves_left
                        }
                        return
                    elif action == "exit":   # Выход из игры через кнопку выхода
                        save_game({
                            'dot_grid': dot_grid,
                            'score': score,
                            'moves_left': moves_left
                        })
                        pygame.quit()
                        sys.exit()

                elif menu_button.collidepoint(mouse_pos) and not is_paused:   # Выход в меню из активной игры
                    SAVED_GAME = {
                        'dot_grid': dot_grid,
                        'score': score,
                        'moves_left': moves_left
                    }
                    return

                elif not is_paused and animating_phase == "idle":   # Начало соед инения точек
                    is_dragging = True
                    current_path = []
                    current_color = None

                    for row in dot_grid:   # Смотрим на какую точку кликнули
                        for dot in row:
                            if dot and is_dot_clicked(dot, mouse_pos, DOT_RADIUS):
                                current_path = [dot]
                                current_color = dot['color']
                                break
                        if current_path:
                            break

            elif event.type == pygame.MOUSEBUTTONUP and not is_paused and animating_phase == "idle":   # Если отпустили цепочку
                is_dragging = False

                if len(current_path) >= 2:   # При длине цепочки больше 2
                    score += len(current_path) * (len(current_path) - 1)   # Подсчет очков
                    moves_left -= 1  # Уменьшение количества ходов
                    for dot in current_path:   # Удаление соединенных точек
                        row = dot['row']
                        col = dot['col']
                        dot_grid[row][col] = None
                    new_dots_to_add = drop_dots(dot_grid)   # Добавление новых точек на пустые места
                    animating_phase = "falling"   # Смена фазы анимации на падение

                current_path = []   # Обнуление данных текущей цепочки
                current_color = None
        if not is_paused:
            if moves_left == 0:   # При окончании количества ходов
                save_score(score)   # Сохранение рекорда
                SAVED_GAME = None   # Удаление сохранения игры
                action = show_game_over(screen, font, score)   # Показ меню об окончании
            if action == "restart":  # Кнопка заново
                main()
                return
            elif action == "menu":  # Кнопка меню
                return

            if is_dragging and current_path and animating_phase == "idle":   # Обработка соединения точек
                mouse_pos = pygame.mouse.get_pos()
                for row in dot_grid:
                    for dot in row:
                        if dot and is_dot_clicked(dot, mouse_pos, DOT_RADIUS):   # Проверка наведения на точку (соседнюю)
                            if dot['color'] == current_color:   # При одинаковом цвете
                                if dot not in current_path:   # Если точка еще не добавлена то добавляем
                                    last_dot = current_path[-1]
                                    if are_dots_adjacent(dot, last_dot):
                                        current_path.append(dot)
                                else:   # При наведении на текущую удаляем
                                    if len(current_path) >= 2 and dot == current_path[-2]:
                                        current_path.pop()

            if animating_phase == "falling":   # Анимация падения
                animating: bool = False

                for row in dot_grid:
                    for dot in row:
                        if dot and 'target_y' in dot and dot['y'] < dot['target_y']:
                            dot['y'] += ANIMATION_SPEED
                            if dot['y'] > dot['target_y']:
                                dot['y'] = dot['target_y']
                            animating = True

                if not animating:
                    animating_phase = "growing"
                    for new_dot in new_dots_to_add:
                        r = new_dot['row']
                        c = new_dot['col']
                        dot_grid[r][c] = new_dot
                    new_dots_to_add = []

            elif animating_phase == "growing":  # Анимация появления
                animating = False
                for row in dot_grid:
                    for dot in row:
                        if dot and dot.get('current_radius', DOT_RADIUS) < DOT_RADIUS:
                            dot['current_radius'] += GROW_SPEED
                            if dot['current_radius'] > DOT_RADIUS:
                                dot['current_radius'] = DOT_RADIUS
                            animating = True

                if not animating:
                    animating_phase = "idle"

            if len(current_path) >= 2: # Отрисовка линий соединенных точек
                for i in range(len(current_path)-1):
                    start_dot = current_path[i]
                    end_dot = current_path[i+1]
                    pygame.draw.line(screen, start_dot['color'], (start_dot['x'], start_dot['y']), (end_dot['x'], end_dot['y']), 10)

            for row in dot_grid:   # Отрисовка всех точек
                for dot in row:
                    if dot:
                        radius = dot.get('current_radius', DOT_RADIUS)
                        if dot in current_path:   # Увеличенный радиус для выделенной
                            radius += 8

                        shadow_offset: int = 4   # Смещение для тени
                        shadow_color: Tuple[int,int,int] = (int(dot['color'][0] * 0.5),
                                      int(dot['color'][1] * 0.5),
                                      int(dot['color'][2] * 0.5))   # Затемнение цвета для тени
                        pygame.draw.circle(screen, shadow_color,
                                         (dot['x'] + shadow_offset, dot['y'] + shadow_offset),
                                         radius-1)   # Отрисовка тени
                        pygame.draw.circle(screen, dot['color'],
                                         (dot['x'], dot['y']), radius)   # Отрисовка точки
        else:   # Затемнение экрана в паузе
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            screen.blit(s, (0, 0))

            pause_msg = font.render("Игра на паузе", True, (255, 255, 255))
            screen.blit(pause_msg, (SCREEN_WIDTH // 2 - pause_msg.get_width() // 2, SCREEN_HEIGHT // 2 - pause_msg.get_height() // 2))

        # Кнопки
        moves_left_text = font.render(f"Ходы: {moves_left}", True, (0, 0, 0))
        score_text = font.render(f"Очки: {score}", True, (0, 0, 0))
        screen.blit(moves_left_text, (10, 50))
        screen.blit(score_text, (10, 10))

        pygame.draw.rect(screen, (100, 150, 250), menu_button, border_radius=12)
        screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2))
        if is_paused:
            pause_button_color: Tuple[int, int, int] = (200, 100, 100)
        else:
            pause_button_color: Tuple[int, int, int] = (100, 150, 250)
        pygame.draw.rect(screen, pause_button_color, pause_button, border_radius=12)
        screen.blit(pause_text, (pause_button.centerx - pause_text.get_width() // 2, pause_button.centery - pause_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)

    from settings import SAVED_GAME

    # Загружаем сохранение
    saved_game_data: Optional[Dict[str, Any]] = load_game()

    if saved_game_data:
        SAVED_GAME = saved_game_data
    else:
        SAVED_GAME = None
    # Чтобы новые точки соеденялись со старыми переделываем старые обратно в кортэж (т.к. при сохранении они сделались списком)
    if SAVED_GAME:
        dot_grid = SAVED_GAME['dot_grid']
        score = SAVED_GAME['score']
        moves_left = SAVED_GAME['moves_left']
        for row in dot_grid:
            for dot in row:
                if dot:
                    dot['color'] = tuple(dot['color'])


    while True:
        action: Optional[str] = show_menu(screen, font, saved_game_exists=(SAVED_GAME is not None) and (SAVED_GAME['moves_left'] > 0)) # Второе условие от сохранения законченной игры

        if action == "continue" and SAVED_GAME:
            main(saved_game=SAVED_GAME)
        elif action == "start":
            SAVED_GAME = None
            main()
        elif action == "rules":
            show_rules(screen, font)
        elif action == "exit":
            pygame.quit()
            sys.exit()