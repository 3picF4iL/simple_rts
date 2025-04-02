import arcade
from utils.i18n import t
from core.entities.unit import *
from core.entities.common import Entity

class Building(arcade.Sprite, Entity):
    def __init__(self, x, y, width=60, height=60):
        super().__init__(center_x=x, center_y=y, width=width, height=height)
        self.selected = False
        self.production_queue = []
        self.base_production_time = 1.0
        self.spawn_point = [self.center_x + 100, self.center_y]

    def add_to_queue(self, unit_cls):
        self.production_queue.append({
            "unit_cls": unit_cls,
            "progress": 0.0,
            "result": "0"
            })

    def process_queue(self, dt, unit_manager):
        if not self.production_queue:
            return

        current = self.production_queue[0]
        current["progress"] += dt * self.base_production_time

        if current["progress"] >= current["unit_cls"].CREATION_TIME:
            unit_manager.spawn_unit(current["unit_cls"].NAME, *self.spawn_point)
            self.production_queue.pop(0)
            return

        current["result"] = f"{min(99, int(current['progress'] / current['unit_cls'].CREATION_TIME * 100))}"

    def get_production_queue_lines(self):
        lines = []
        if not self.production_queue:
            return lines

        for q in self.production_queue[:5]:
            unit_cls = q["unit_cls"]
            if not unit_cls:
                continue
            lines.append(f"{unit_cls.NAME} ({q['result']}%)")
        return lines

    def update(self, dt, unit_manager):
        self.process_queue(dt, unit_manager)

# ------------------------------
# Building types
# ------------------------------

class MilitaryBuilding(Building):
    def __init__(self, x, y, width=60, height=60):
        super().__init__(x, y, width, height)
        self.building_type = "military"


class EconomicBuilding(Building):
    def __init__(self, x, y, width=60, height=60):
        super().__init__(x, y, width, height)
        self.building_type = "economic"


# ------------------------------
# Buildings list
# ------------------------------

class Barracks(MilitaryBuilding):
    NAME = 'barracks'
    DESCRIPTION = 'barracks_info'
    def __init__(self, x, y):
        width = 100
        height = 100

        texture = arcade.make_soft_square_texture(100, arcade.color.RED, 255)
        super().__init__(x, y, width, height)
        self.texture = texture
        self.unit_production_options = ["test_unit", "test_unit2"]
