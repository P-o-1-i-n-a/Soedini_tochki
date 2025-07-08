import pygame
import random
from settings import *
from typing import *

def is_dot_clicked(dot: Dict[str,Any], mouse_pos: Tuple[int, int], dot_radius: int)-> bool:   # Проверка на клик по точке
    dx = dot['x'] - mouse_pos[0]
    dy = dot['y'] - mouse_pos[1]
    distance_squared = dx * dx + dy * dy
    return distance_squared <= dot_radius * dot_radius


def are_dots_adjacent(dot1: Dict[str, int], dot2: Dict[str, int])-> bool:   # Проверка на соседние точки
    return abs(dot1['row'] - dot2['row']) <= 1 and abs(dot1['col'] - dot2['col']) <= 1


def drop_dots(dot_grid: List[List[Optional[Dict[str, Any]]]])-> List[Dict[str, float]]:   # Падение точек
    margin = 50
    spacing = (SCREEN_WIDTH - 2 * margin) // (GRID_SIZE - 1)
    new_dots_to_add = []

    for col in range(GRID_SIZE):
        empty_slots = 0

        for row in reversed(range(GRID_SIZE)):   # Снизу вверх обработка
            if dot_grid[row][col] is None:
                empty_slots += 1
            elif empty_slots > 0:
                new_row = row + empty_slots
                dot_grid[new_row][col] = dot_grid[row][col]   # Перемещение вниз точки
                dot_grid[new_row][col]['row'] = new_row
                dot_grid[new_row][col]['target_y'] = margin + new_row * spacing + 160   #
                dot_grid[new_row][col]['current_radius'] = DOT_RADIUS
                dot_grid[row][col] = None   # Освобождение старой точки

        for i in range(empty_slots):  # Заполнение новых точек
            row = i
            x = margin + col * spacing
            y = margin + row * spacing + 160
            color = random.choice(COLORS)
            new_dots_to_add.append({
                'x': x,
                'y': y,
                'target_y': y,
                'color': color,
                'row': row,
                'col': col,
                'current_radius': 1
            })

    return new_dots_to_add


def init_dot_grid()-> List[List[Dict[str, Any]]]:   # Игровое поле
    dot_grid: List[List[Dict[str, Any]]]  = []
    margin = 50
    spacing = (SCREEN_WIDTH - 2 * margin) // (GRID_SIZE - 1)

    for row in range(GRID_SIZE):   # Заполнение точками
        dot_row = []
        for col in range(GRID_SIZE):
            x = margin + col * spacing
            y = margin + row * spacing + 160
            color = random.choice(COLORS)
            dot_row.append({
                'x': x,
                'y': y,
                'target_y': y,
                'color': color,
                'row': row,
                'col': col,
                'current_radius': DOT_RADIUS
            })
        dot_grid.append(dot_row)

    return dot_grid