import arcade
from utils.calc import dist
from utils.i18n import t
from core.entities.common import Entity

class Unit(arcade.Sprite, Entity):
    SPEED = 50  # px/s
    CREATION_TIME = 1  # seconds

    def __init__(self, x, y, texture, color=arcade.color.BLUE, size=20):
        super().__init__(texture, center_x=x, center_y=y, size=size)
        self.target_x = x
        self.target_y = y
        self.selected = False
        self.color = color
        self.actions = ["[PLACEHOLDER] Move", "[PLACEHOLDER] Stop"]

        # Mods
        self.creation_time_mod = 1.0

    def update(self, delta_time, buildings):
        if not self._has_reached_target():
            self._move_towards_target(delta_time)
            if self._collides_with_buildings(buildings):
                self._undo_last_movement(delta_time)

    def _has_reached_target(self):
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y
        return dist(dx, dy) < 1

    def _move_towards_target(self, delta_time):
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y
        d = dist(dx, dy)
        if d == 0:
            return
        self.last_dx = (dx / d) * self.speed * delta_time
        self.last_dy = (dy / d) * self.speed * delta_time
        self.center_x += self.last_dx
        self.center_y += self.last_dy

    def _collides_with_buildings(self, buildings):
        return arcade.check_for_collision_with_list(self, buildings)

    def _undo_last_movement(self, delta_time):
        self.center_x -= self.last_dx
        self.center_y -= self.last_dy

    def draw(self):
        if self.selected:
            arcade.draw_lrbt_rectangle_outline(self.center_x, self.center_y, 24, 24, arcade.color.YELLOW, 2)

    # Getters
    @property
    def final_creation_time(self):
        return self.CREATION_TIME * self.creation_time_mod


class TestUnit(Unit):
    NAME = "test_unit"
    DESCRIPTION = "test_unit_desc"

    def __init__(self, x, y, size=20):
        color = arcade.color.GREEN
        texture = arcade.make_soft_square_texture(size, color, 255)
        super().__init__(x, y, texture, color, size)
        self.speed = 100
        self.actions = ["Move", "Attack", "Defend"]

class TestUnit2(Unit):
    NAME = "test_unit2"
    DESCRIPTION = "test_unit_desc2"

    def __init__(self, x, y, size=20):
        color = arcade.color.ORANGE
        texture = arcade.make_soft_square_texture(size, color, 255)
        super().__init__(x, y, texture, color, size)
        self.speed = 80
        self.actions = ["Move", "Attack", "Defend"]

