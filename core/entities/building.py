import arcade
from utils.i18n import t

class Building(arcade.Sprite):
    def __init__(self, x, y, width=60, height=60):
        super().__init__(center_x=x, center_y=y, width=width, height=height)
        self.selected = False

    def get_hover_info(self) -> str:
        return "Building"

    def get_actions(self) -> list:
        return []

# ------------------------------
# Building types
# ------------------------------

class MilitaryBuilding(Building):
    def get_hover_info(self) -> str:
        return "Military Building"


class EconomicBuilding(Building):
    def get_hover_info(self) -> str:
        return "Economic Building"


# ------------------------------
# Buildings list
# ------------------------------

class Barracks(MilitaryBuilding):
    def __init__(self, x, y):
        width = 100
        height = 100
        self.name = "barracks"

        texture = arcade.make_soft_square_texture(100, arcade.color.RED, 255)
        super().__init__(x, y, width, height)
        self.texture = texture

    def get_hover_info(self) -> str:
        return f"{t(self.name)}: {t('barracks_hover_info')}"

    def get_actions(self) -> list:
        return [
            {"label": f"{t('create_unit')}", "action": "create_unit"}
        ]
