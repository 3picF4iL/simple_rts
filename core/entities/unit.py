import arcade
from utils.calc import dist
from utils.i18n import t


class Unit(arcade.Sprite):
    ENTITY_TYPE = 'unit'

    def __init__(self, x, y, config):
        size = config.get("size", 20)
        color = getattr(arcade.color, config.get("color", "BLUE"))
        texture = arcade.make_soft_square_texture(size, color, 255)

        super().__init__(texture, center_x=x, center_y=y, width=size, height=size)
        self.target_x = x
        self.target_y = y
        self.selected = False

        # Configurable attributes
        self.name = config.get("name", "unit")
        self.description = config.get("description", "")
        self.speed = config.get("speed", 50)
        self.creation_time = config.get("creation_time", 1)
        self.cost = config.get("cost", {})
        self.actions = config.get("actions", [])
        self.production_options = config.get("production_options", [])
        self.type = config.get("type", [])

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
        super().draw()
        if self.selected:
            arcade.draw_lrbt_rectangle_outline(
                self.center_x - 12,
                self.center_x + 12,
                self.center_y - 12,
                self.center_y + 12,
                arcade.color.YELLOW, 2)

    @property
    def final_creation_time(self):
        return self.creation_time * self.creation_time_mod
