import arcade


class Unit(arcade.Sprite):
    def __init__(self, x, y):
        texture = arcade.make_soft_square_texture(20, arcade.color.BLUE, 255)
        super().__init__(texture, center_x=x, center_y=y)
        self.speed = 100  # px/s
        self.target_x = x
        self.target_y = y
        self.selected = False

    def update(self, delta_time, buildings):
        if not self._has_reached_target():
            self._move_towards_target(delta_time)
            if self._collides_with_buildings(buildings):
                self._undo_last_movement(delta_time)

    def _has_reached_target(self):
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y
        return (dx**2 + dy**2) ** 0.5 < 1

    def _move_towards_target(self, delta_time):
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        self.last_dx = (dx / distance) * self.speed * delta_time
        self.last_dy = (dy / distance) * self.speed * delta_time
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
