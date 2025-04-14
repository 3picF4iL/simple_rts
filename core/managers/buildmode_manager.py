import arcade

class BuildModeManager:
    def __init__(self, building_manager):
        self.active_cls = None
        self.valid_placement = False
        self._check_timer = 0.0
        self._check_interval = 0.1
        self.building_manager = building_manager
        self.ghost = None
        self.ghost_list = arcade.SpriteList()

    def start(self, cls):
        self.active_cls = cls
        self.ghost = cls(0, 0)
        self.ghost.alpha = 50
        self.ghost_list.append(self.ghost)

    def cancel(self):
        self.active_cls = None
        self.ghost_list.clear()

    def is_active(self):
        return self.active_cls and self.ghost_list

    def update(self, x, y, blocked):
        if not self.ghost_list:
            return

        self.ghost.center_x = x
        self.ghost.center_y = y

        self.valid_placement = not arcade.check_for_collision_with_lists(self.ghost, blocked)
        self.ghost.color = arcade.color.GREEN if self.valid_placement else arcade.color.RED

    def draw(self):
        if self.is_active() and self.ghost_list:
            self.ghost_list.draw()

    def should_place(self):
        return self.valid_placement

    def place(self):
        if self.ghost and self.valid_placement and self.active_cls:
            self.building_manager.add_building(self.active_cls.NAME, self.ghost.center_x, self.ghost.center_y)
            self.cancel()