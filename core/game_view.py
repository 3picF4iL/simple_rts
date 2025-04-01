import arcade
from core.managers.building_manager import BuildingManager
from core.managers.unit_manager import UnitManager
from core.managers.selection_manager import SelectionManager
from utils.i18n import t


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.buildings = None
        self.unit_manager = None
        self.selection_manager = None
        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)

        self.unit_manager = UnitManager()
        self.selection_manager = SelectionManager()
        self.building_manager = BuildingManager()

    def on_show_view(self):
        print("On show")
        self.building_manager.add_building(300, 300)
        self.building_manager.add_building(600, 400)
        self.unit_manager.spawn_unit(100, 300)
        self.unit_manager.spawn_unit(400, 100)

    def on_draw(self):
        self.clear()
        self.unit_manager.draw()
        self.building_manager.draw()
        self.selection_manager.draw()

    def on_update(self, delta_time):
        self.unit_manager.update(delta_time, self.building_manager.buildings)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.selection_manager.start_selection(x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.unit_manager.command_move(
                self.selection_manager.selected_objects,
                x, y
            )

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            dx = abs(self.selection_manager.start_x - x)
            dy = abs(self.selection_manager.start_y - y)

            if dx < 5 and dy < 5:
                self.selection_manager.select_by_click(
                    self.unit_manager.get_units(),
                    self.building_manager.get_buildings(),
                    x, y
                )
            else:
                self.selection_manager.select_by_box(
                    self.unit_manager.get_units(),
                    self.selection_manager.start_x,
                    self.selection_manager.start_y,
                    x, y
                )

        self.selection_manager.selecting = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.selection_manager.selecting:
            self.selection_manager.update_selection(x, y)
