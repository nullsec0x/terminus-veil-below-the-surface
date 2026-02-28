"""Player class for Terminus Veil."""

from .items import Inventory


class Player:
    """Represents the deep‑sea diver."""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.symbol = '◉'
        self.hp = 100                # oxygen
        self.max_hp = 100
        self.attack_power = 10       # harpoon strength
        self.inventory = Inventory()
    
    def move(self, dx: int, dy: int, game_map) -> bool:
        new_x = self.x + dx
        new_y = self.y + dy
        if (0 <= new_x < len(game_map[0]) and 
            0 <= new_y < len(game_map) and 
            game_map[new_y][new_x] != '#'):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def take_damage(self, damage: int):
        self.hp = max(0, self.hp - damage)
    
    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)
    
    def is_alive(self) -> bool:
        return self.hp > 0
