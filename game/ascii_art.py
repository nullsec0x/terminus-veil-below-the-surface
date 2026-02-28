"""ASCII art and visual improvements for Terminus Veil."""

from typing import Dict, Tuple


class ASCIIChars:
    """Contains all ASCII characters used in the game (underwater theme)."""
    
    # Player
    PLAYER = "◉"          # diver / submersible
    
    # Sea creatures
    JELLYFISH = "〰"
    ANGLERFISH = "☉"
    LEVIATHAN = "◈"
    CORPSE = "☠"
    
    # Items
    OXYGEN_TANK = "⊕"
    RESEARCH_DATA = "◌"
    SIGNAL_FLARE = "✦"
    HARPOON_UPGRADE = "†"    # unchanged
    
    # Terrain
    FLOOR = "·"               # open water
    EXIT = "▼"                # descent marker
    
    # Walls (rock formations) – same line characters, different color
    WALL_HORIZONTAL = "═"
    WALL_VERTICAL = "║"
    WALL_TOP_LEFT = "╔"
    WALL_TOP_RIGHT = "╗"
    WALL_BOTTOM_LEFT = "╚"
    WALL_BOTTOM_RIGHT = "╝"
    WALL_CROSS = "╬"
    WALL_T_UP = "╩"
    WALL_T_DOWN = "╦"
    WALL_T_LEFT = "╣"
    WALL_T_RIGHT = "╠"
    
    WALL_EXPLORED = "▓"
    FLOOR_EXPLORED = "░"


class WallRenderer:
    """Handles intelligent wall rendering (unchanged logic, only visual)."""
    
    def __init__(self, game_map):
        self.game_map = game_map
        self.height = len(game_map)
        self.width = len(game_map[0]) if game_map else 0
    
    def get_wall_char(self, x: int, y: int) -> str:
        if not self._is_wall(x, y):
            return ASCIIChars.FLOOR
        
        up = self._is_wall(x, y - 1)
        down = self._is_wall(x, y + 1)
        left = self._is_wall(x - 1, y)
        right = self._is_wall(x + 1, y)
        
        connections = (up, right, down, left)
        
        if connections == (True, True, True, True):
            return ASCIIChars.WALL_CROSS
        elif connections == (False, True, True, True):
            return ASCIIChars.WALL_T_DOWN
        elif connections == (True, False, True, True):
            return ASCIIChars.WALL_T_RIGHT
        elif connections == (True, True, False, True):
            return ASCIIChars.WALL_T_UP
        elif connections == (True, True, True, False):
            return ASCIIChars.WALL_T_LEFT
        elif connections == (False, False, True, True):
            return ASCIIChars.WALL_TOP_LEFT
        elif connections == (False, True, True, False):
            return ASCIIChars.WALL_TOP_RIGHT
        elif connections == (True, False, False, True):
            return ASCIIChars.WALL_BOTTOM_LEFT
        elif connections == (True, True, False, False):
            return ASCIIChars.WALL_BOTTOM_RIGHT
        elif connections in [(True, False, True, False), (False, False, False, False)]:
            return ASCIIChars.WALL_VERTICAL
        elif connections == (False, True, False, True):
            return ASCIIChars.WALL_HORIZONTAL
        else:
            return ASCIIChars.WALL_VERTICAL if (up or down) else ASCIIChars.WALL_HORIZONTAL
    
    def _is_wall(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.game_map[y][x] == '#'


class ColorScheme:
    """Underwater color palette."""
    
    # Player
    PLAYER = "[bold bright_cyan]"
    
    # Creatures
    JELLYFISH = "[light_blue]"
    ANGLERFISH = "[purple]"
    LEVIATHAN = "[bold dark_red]"
    CORPSE = "[dim white]"
    
    # Items
    OXYGEN_TANK = "[cyan]"
    RESEARCH_DATA = "[aqua]"
    SIGNAL_FLARE = "[bright_yellow]"
    HARPOON_UPGRADE = "[bright_white]"
    
    # Terrain
    WALL = "[bright_white]"          # rock (visible)
    WALL_EXPLORED = "[dim white]"    # rock (previously seen)
    FLOOR = "[dim cyan]"             # open water (visible)
    FLOOR_EXPLORED = "[dim black]"   # open water (previously seen)
    EXIT = "[bright_green]"
    
    RESET = "[/]"


def get_colored_char(char: str, color: str) -> str:
    return f"{color}{char}{ColorScheme.RESET}"


def get_entity_display(entity_type: str, is_alive: bool = True) -> str:
    """Get colored character for a creature."""
    if not is_alive:
        return get_colored_char(ASCIIChars.CORPSE, ColorScheme.CORPSE)
    
    entity_map = {
        'player': (ASCIIChars.PLAYER, ColorScheme.PLAYER),
        'jellyfish': (ASCIIChars.JELLYFISH, ColorScheme.JELLYFISH),
        'anglerfish': (ASCIIChars.ANGLERFISH, ColorScheme.ANGLERFISH),
        'leviathan': (ASCIIChars.LEVIATHAN, ColorScheme.LEVIATHAN),
    }
    
    if entity_type in entity_map:
        char, color = entity_map[entity_type]
        return get_colored_char(char, color)
    
    return entity_type


def get_item_display(item_type: str) -> str:
    """Get colored character for an item."""
    item_map = {
        'oxygen_tank': (ASCIIChars.OXYGEN_TANK, ColorScheme.OXYGEN_TANK),
        'research_data': (ASCIIChars.RESEARCH_DATA, ColorScheme.RESEARCH_DATA),
        'signal_flare': (ASCIIChars.SIGNAL_FLARE, ColorScheme.SIGNAL_FLARE),
        'harpoon_upgrade': (ASCIIChars.HARPOON_UPGRADE, ColorScheme.HARPOON_UPGRADE),
    }
    
    if item_type in item_map:
        char, color = item_map[item_type]
        return get_colored_char(char, color)
    
    return item_type
