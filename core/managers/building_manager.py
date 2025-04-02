import arcade
from core.entities.building import *

class BuildingManager:
    def __init__(self):
        self.buildings = arcade.SpriteList(use_spatial_hash=True)
        self.buildings_map = {
            "barracks": Barracks
        }

    def add_building(self, name, x, y):
        building = self.buildings_map.get(name, None)(x, y)
        if not building:
            raise Exception("Building not available!")
        self.buildings.append(building)

    def get_buildings(self):
        return self.buildings

    def draw(self):
        self.buildings.draw()
        for building in self.buildings:
            if building.selected:
                arcade.draw_lrbt_rectangle_outline(
                    building.center_x - building.width / 2,
                    building.center_x + building.width / 2,
                    building.center_y - building.height / 2,
                    building.center_y + building.height / 2,
                    arcade.color.YELLOW,
                    2
                )
    def update(self, dt, unit_manager):
        for building in self.buildings:
            if hasattr(building, "update"):
                building.update(dt, unit_manager)
