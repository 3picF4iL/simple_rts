import arcade
from core.entities.building import Building

class BuildingManager:
    def __init__(self, definitions, entity_factory):
        self.buildings = arcade.SpriteList(use_spatial_hash=True)
        self.definitions = definitions
        self.entity_factory = entity_factory

    def add_building(self, x, y, name, add_to_list=True):
        building = Building(x, y, self.definitions[name])
        building.entity_factory = self.entity_factory
        if add_to_list:
            self.buildings.append(building)
            return
        return building

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
            building.update(dt, unit_manager)
