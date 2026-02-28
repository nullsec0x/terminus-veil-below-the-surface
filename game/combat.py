"""Combat system for Terminus Veil."""

import random
from typing import List, Tuple, Optional
from .monster import Monster


class CombatSystem:
    """Handles underwater combat and turn order."""
    
    def __init__(self):
        self.turn_count = 0
        self.combat_log: List[str] = []
    
    def player_attack_monster(self, player, monster: Monster) -> List[str]:
        messages = []
        if not monster.is_alive:
            messages.append(f"The {monster.name} is already dead.")
            return messages

        base_damage = player.attack_power
        damage = random.randint(max(1, base_damage - 2), base_damage + 3)
        
        monster_died = monster.take_damage(damage)
        
        messages.append(f"You fire your harpoon at the {monster.name} for {damage} damage!")
        
        if monster_died:
            messages.append(f"The {monster.name} dissolves into the deep.")
        else:
            messages.append(f"The {monster.name} has {monster.hp}/{monster.max_hp} health remaining.")
        
        return messages
    
    def monster_attack_player(self, monster: Monster, player) -> List[str]:
        messages = []
        if not monster.is_alive:
            return messages
        
        damage = monster.attack(player)
        player.take_damage(damage)
        
        messages.append(f"The {monster.name} strikes you for {damage} damage!")
        
        if not player.is_alive():
            messages.append("Oxygen depleted! Mission failed.")
        else:
            messages.append(f"You have {player.hp}/{player.max_hp} oxygen remaining.")
        
        return messages
    
    def process_turn(self, player, monster_manager, game_map, visibility_tracker) -> List[str]:
        self.turn_count += 1
        all_messages = []
        
        monster_messages = monster_manager.update_monsters(
            player.x, player.y, game_map, visibility_tracker
        )
        all_messages.extend(monster_messages)
        
        for monster in monster_manager.monsters:
            if (monster.is_alive and 
                monster.is_adjacent_to(player.x, player.y) and
                visibility_tracker.is_visible(monster.x, monster.y)):
                
                combat_messages = self.monster_attack_player(monster, player)
                all_messages.extend(combat_messages)
        
        monster_manager.remove_dead_monsters()
        
        self.combat_log.extend(all_messages)
        if len(self.combat_log) > 10:
            self.combat_log = self.combat_log[-10:]
        
        return all_messages
    
    def get_recent_messages(self, count: int = 5) -> List[str]:
        return self.combat_log[-count:] if self.combat_log else []
    
    def clear_log(self):
        self.combat_log.clear()


class GameState:
    """Manages overall dive state and win/lose conditions."""
    
    def __init__(self):
        self.game_over = False
        self.victory = False
        self.current_level = 1
        self.score = 0
    
    def check_victory_condition(self, player_x: int, player_y: int, game_map) -> bool:
        if (0 <= player_x < len(game_map[0]) and 
            0 <= player_y < len(game_map) and
            game_map[player_y][player_x] == '>'):
            self.victory = True
            return True
        return False
    
    def check_defeat_condition(self, player) -> bool:
        if not player.is_alive():
            self.game_over = True
            return True
        return False
    
    def advance_level(self):
        self.current_level += 1
        self.victory = False
        self.score += 100 * self.current_level
    
    def get_monster_count_for_level(self) -> int:
        return min(3 + self.current_level, 10)
    
    def get_item_count_for_level(self) -> int:
        return min(5 + self.current_level, 12)
    
    def add_score(self, points: int):
        self.score += points
