import arcade
from utils.i18n import t

class Building(arcade.Sprite):
    ENTITY_TYPE = 'building'

    def __init__(self, x, y, config):
        size = config.get("size", 60)
        color = getattr(arcade.color, config.get("color", "WHITE"))
        texture = arcade.make_soft_square_texture(size, color, 255)

        super().__init__(texture, center_x=x, center_y=y, width=size, height=size)

        self.selected = False
        self.name = config.get("name", "building")
        self.description = config.get("description", "")
        self.etype = config.get("etype")
        self.building_type = config.get("type", "unknown")
        self.production_options = config.get("production_options", [])
        self.production_queue = []
        self.base_production_time = 1.0
        self.spawn_point = [self.center_x + 100, self.center_y]

        self.entity_factory = None  # to be injected externally

    def add_to_queue(self, unit_name):
        self.production_queue.append({
            "unit_name": unit_name,
            "progress": 0.0,
            "result": "0"
        })

    def process_queue(self, dt, unit_manager):
        if not self.production_queue or not self.entity_factory:
            return

        current = self.production_queue[0]
        creation_time = self.entity_factory.get_creation_time(current["unit_name"])
        current["progress"] += dt * self.base_production_time

        if current["progress"] >= creation_time:
            unit = self.entity_factory.create_unit(current["unit_name"], *self.spawn_point)
            unit_manager.units.append(unit)
            self.production_queue.pop(0)
            return

        current["result"] = f"{min(99, int(current['progress'] / creation_time * 100))}"

    def get_production_queue_lines(self):
        lines = []
        for q in self.production_queue[:5]:
            lines.append(f"{q['unit_name']} ({q['result']}%)")
        return lines

    def update(self, dt, unit_manager):
        self.process_queue(dt, unit_manager)

    def kill(self):
        self.production_queue.clear()
        super().kill()

    def draw(self):
        super().draw()
        if self.selected:
            arcade.draw_lrbt_rectangle_outline(
                self.center_x - self.width // 2,
                self.center_x + self.width // 2,
                self.center_y - self.height // 2,
                self.center_y + self.height // 2,
                arcade.color.YELLOW, 2
            )