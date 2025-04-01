import arcade
from core.entities.building import Building

class BuildingManager:
    def __init__(self):
        self.buildings = arcade.SpriteList(use_spatial_hash=True)

    def add_building(self, x, y):
        building = Building(x, y)
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