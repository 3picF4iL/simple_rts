import arcade
from utils.i18n import t
from core.entities.unit import *
from core.entities.common import Entity

class Building(arcade.Sprite, Entity):
    def __init__(self, x, y, width=60, height=60):
        super().__init__(center_x=x, center_y=y, width=width, height=height)
        self.selected = False

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
