import arcade
from core.entities.unit import *

class UnitManager:
    def __init__(self):
        self.units = arcade.SpriteList()
        self.unit_map = {
            "test_unit": TestUnit,
            "test_unit2": TestUnit2,
        }


    def spawn_unit(self, unit_type, x, y):
        unit_cls = self.unit_map.get(unit_type)
        if not unit_cls:
            print(f"[UnitManager] Unknown unit type: {unit_type}")
            return
        unit = unit_cls(x, y)
        self.units.append(unit)

    def update(self, delta_time, buildings):
        for unit in self.units:
            unit.update(delta_time, buildings)

    def draw(self):
        self.units.draw()
        self.draw_selected()

    def draw_selected(self):
        for unit in self.units:
            if unit.selected:
                arcade.draw_lrbt_rectangle_outline(
                    unit.center_x - unit.width / 2,
                    unit.center_x + unit.width / 2,
                    unit.center_y - unit.height / 2,
                    unit.center_y + unit.height / 2,
                    arcade.color.YELLOW,
                    2
                )

    def get_units(self):
        return self.units

    def command_move(self, selected_units, x, y):
        for unit in selected_units:
            unit.target_x = x
            unit.target_y = y
