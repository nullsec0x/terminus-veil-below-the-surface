"""Field of View system (unchanged logic)."""

import math
from typing import Set, Tuple, List


class FOVCalculator:
    """Calculates field of view using shadowcasting."""
    
    def __init__(self, game_map: List[List[str]]):
        self.game_map = game_map
        self.width = len(game_map[0]) if game_map else 0
        self.height = len(game_map)
    
    def calculate_fov(self, player_x: int, player_y: int, 
                      radius: int = 8) -> Set[Tuple[int, int]]:
        visible = set()
        visible.add((player_x, player_y))
        for direction in range(8):
            self._cast_ray(player_x, player_y, direction, radius, visible)
        return visible
    
    def _cast_ray(self, start_x: int, start_y: int, direction: int, 
                  radius: int, visible: Set[Tuple[int, int]]):
        directions = [
            (0, -1), (1, -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0), (-1, -1)
        ]
        dx, dy = directions[direction]
        for distance in range(1, radius + 1):
            x = start_x + dx * distance
            y = start_y + dy * distance
            if not (0 <= x < self.width and 0 <= y < self.height):
                break
            visible.add((x, y))
            if self.game_map[y][x] == '#':
                break
    
    def calculate_simple_fov(self, player_x: int, player_y: int, 
                           radius: int = 8) -> Set[Tuple[int, int]]:
        visible = set()
        for y in range(max(0, player_y - radius), 
                      min(self.height, player_y + radius + 1)):
            for x in range(max(0, player_x - radius), 
                          min(self.width, player_x + radius + 1)):
                distance = math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
                if distance <= radius and self._has_line_of_sight(player_x, player_y, x, y):
                    visible.add((x, y))
        return visible
    
    def _has_line_of_sight(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        x_inc = 1 if x1 < x2 else -1
        y_inc = 1 if y1 < y2 else -1
        error = dx - dy
        while True:
            if (x, y) != (x1, y1) and self.game_map[y][x] == '#':
                return False
            if x == x2 and y == y2:
                break
            error2 = 2 * error
            if error2 > -dy:
                error -= dy
                x += x_inc
            if error2 < dx:
                error += dx
                y += y_inc
        return True


class VisibilityTracker:
    """Tracks explored vs visible areas."""
    
    def __init__(self):
        self.explored: Set[Tuple[int, int]] = set()
        self.visible: Set[Tuple[int, int]] = set()
    
    def update_visibility(self, new_visible: Set[Tuple[int, int]]):
        self.visible = new_visible
        self.explored.update(new_visible)
    
    def is_visible(self, x: int, y: int) -> bool:
        return (x, y) in self.visible
    
    def is_explored(self, x: int, y: int) -> bool:
        return (x, y) in self.explored
