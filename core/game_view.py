import arcade
from core.managers.building_manager import BuildingManager
from core.managers.unit_manager import UnitManager
from core.managers.selection_manager import SelectionManager
from core.managers.gui_manager import GUIManager
from core.managers.input_manager import InputManager
from core.game_controller import GameController
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
        self.controller = GameController(self.unit_manager, self.building_manager, None)
        self.gui = GUIManager(self.window, self.controller)
        self.controller.gui_manager = self.gui
        self.input = InputManager(self.gui, self.selection_manager, self.unit_manager, self.building_manager)

    def on_show_view(self):
        self.building_manager.add_building('barracks', 300, 300)
        self.unit_manager.spawn_unit(200, 300)

    def on_draw(self):
        self.clear()
        self.unit_manager.draw()
        self.building_manager.draw()
        self.selection_manager.draw()
        self.gui.draw()

    def on_update(self, delta_time):
        self.unit_manager.update(delta_time, self.building_manager.buildings)

    def on_mouse_press(self, x, y, button, modifiers):
        self.input.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.input.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.input.on_mouse_motion(x, y, dx, dy)
