"""Item and inventory system for Terminus Veil."""

import random
from typing import List, Dict, Optional, Tuple
from enum import Enum


class ItemType(Enum):
    """Underwater item types."""
    OXYGEN_TANK = ("⊕", "Oxygen Tank", "Restores 25 oxygen")
    RESEARCH_DATA = ("◌", "Research Data", "Valuable research data")
    SIGNAL_FLARE = ("✦", "Signal Flare", "A flare that may attract help?")
    HARPOON_UPGRADE = ("†", "Harpoon Upgrade", "Increases harpoon strength")


class Item:
    """Represents an item in the underwater world."""
    
    def __init__(self, x: int, y: int, item_type: ItemType, value: int = 1):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.symbol = item_type.value[0]
        self.name = item_type.value[1]
        self.description = item_type.value[2]
        self.value = value
        self.is_collected = False
    
    def use(self, player) -> str:
        """Use the item on the diver."""
        if self.item_type == ItemType.OXYGEN_TANK:
            heal_amount = min(25, player.max_hp - player.hp)
            player.hp += heal_amount
            return f"You use the oxygen tank and recover {heal_amount} oxygen!"
        
        elif self.item_type == ItemType.SIGNAL_FLARE:
            effect = random.choice(["heal", "damage_boost", "nothing"])
            if effect == "heal":
                heal_amount = random.randint(10, 30)
                player.hp = min(player.max_hp, player.hp + heal_amount)
                return f"The flare's glow revitalizes you! +{heal_amount} oxygen."
            elif effect == "damage_boost":
                player.attack_power += 2
                return "The flare sharpens your senses! Harpoon Strength +2!"
            else:
                return "The flare fizzles. Nothing happens."
        
        elif self.item_type == ItemType.HARPOON_UPGRADE:
            player.attack_power += 5
            return "You upgrade your harpoon! Strength increased by 5!"
        
        elif self.item_type == ItemType.RESEARCH_DATA:
            return f"You collect {self.value} research data points."
        
        return f"You can't use the {self.name}."


class Inventory:
    """Manages the diver's inventory."""
    
    def __init__(self):
        self.items: Dict[ItemType, int] = {}
        self.data_points = 0   # formerly gold
    
    def add_item(self, item: Item) -> str:
        if item.item_type == ItemType.RESEARCH_DATA:
            self.data_points += item.value
            return f"Collected {item.value} research data!"
        else:
            if item.item_type in self.items:
                self.items[item.item_type] += item.value
            else:
                self.items[item.item_type] = item.value
            return f"Picked up {item.name}!"
    
    def use_item(self, item_type: ItemType, player) -> Optional[str]:
        if item_type not in self.items or self.items[item_type] <= 0:
            return None
        
        temp_item = Item(0, 0, item_type)
        effect_message = temp_item.use(player)
        
        self.items[item_type] -= 1
        if self.items[item_type] <= 0:
            del self.items[item_type]
        
        return effect_message
    
    def get_item_count(self, item_type: ItemType) -> int:
        return self.items.get(item_type, 0)
    
    def get_inventory_display(self) -> str:
        lines = [f"Data: {self.data_points}"]
        for item_type, count in self.items.items():
            lines.append(f"{item_type.value[1]}: {count}")
        return "\n".join(lines) if lines else "Empty"


class ItemManager:
    """Manages all items in the game world."""
    
    def __init__(self):
        self.items: List[Item] = []
    
    def spawn_items(self, game_map, count: int = 8):
        from .dungeon_generator import DungeonGenerator
        
        generator = DungeonGenerator(len(game_map[0]), len(game_map))
        positions = generator.find_valid_positions(game_map, count)
        
        for i, (x, y) in enumerate(positions):
            rand = random.random()
            
            if rand < 0.4:      # 40% research data
                item_type = ItemType.RESEARCH_DATA
                value = random.randint(5, 20)
            elif rand < 0.7:    # 30% oxygen tank
                item_type = ItemType.OXYGEN_TANK
                value = 1
            elif rand < 0.9:    # 20% signal flare
                item_type = ItemType.SIGNAL_FLARE
                value = 1
            else:                # 10% harpoon upgrade
                item_type = ItemType.HARPOON_UPGRADE
                value = 1
            
            item = Item(x, y, item_type, value)
            self.items.append(item)
    
    def get_item_at(self, x: int, y: int) -> Optional[Item]:
        for item in self.items:
            if item.x == x and item.y == y and not item.is_collected:
                return item
        return None
    
    def collect_item(self, x: int, y: int) -> Optional[Item]:
        item = self.get_item_at(x, y)
        if item:
            item.is_collected = True
            return item
        return None
    
    def get_visible_items(self, visibility_tracker) -> List[Item]:
        visible_items = []
        for item in self.items:
            if (not item.is_collected and 
                visibility_tracker.is_visible(item.x, item.y)):
                visible_items.append(item)
        return visible_items
