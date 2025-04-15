import arcade
from core.managers.building_manager import BuildingManager
from core.managers.unit_manager import UnitManager
from core.managers.selection_manager import SelectionManager
from core.managers.gui_manager import GUIManager
from core.managers.input_manager import InputManager
from core.managers.resource_manager import ResourceManager
from core.managers.buildmode_manager import BuildModeManager
from core.game_controller import GameController
from core.factory.entity_factory import EntityFactory
from utils.i18n import t
from utils.loader import load_object_definitions


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.buildings = None
        self.unit_manager = None
        self.selection_manager = None
        self.building_manager = None
        self.build_mode_manager = None
        self.resource_manager = None
        self.controller = None
        self.gui = None
        self.input = None

        self.objects_definitions = {}

        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.objects_definitions = load_object_definitions()

        unit_defs = self.objects_definitions.get('units', {})
        building_defs = self.objects_definitions.get('buildings', {})

        entity_factory = EntityFactory(unit_defs, building_defs)

        self.unit_manager = UnitManager(unit_defs)
        self.selection_manager = SelectionManager()
        self.building_manager = BuildingManager(building_defs, entity_factory)
        self.resource_manager = ResourceManager()
        self.build_mode_manager = BuildModeManager(self.building_manager)
        self.controller = GameController(
            self.unit_manager,
            self.building_manager,
            self.resource_manager,
            None,
            self.build_mode_manager,
            entity_factory
        )
        self.gui = GUIManager(self.window, self.controller)
        self.controller.gui_manager = self.gui
        self.input = InputManager(
            self.gui,
            self.selection_manager,
            self.unit_manager,
            self.building_manager,
            self.build_mode_manager,
            self.controller
        )

    def on_show_view(self):
        # Test purpose
        self.building_manager.add_building(300, 300, 'town_center')
        self.building_manager.add_building(700, 350, 'barracks')
        self.unit_manager.spawn_unit(200, 300, 'villager')

    def on_draw(self):
        self.clear()
        self.unit_manager.draw()
        self.building_manager.draw()
        self.selection_manager.draw()
        self.build_mode_manager.draw()
        self.gui.draw()

    def on_update(self, delta_time):
        self.gui.update(delta_time)
        self.building_manager.update(delta_time, self.unit_manager)
        self.unit_manager.update(delta_time, self.building_manager.buildings)

    def on_mouse_press(self, x, y, button, modifiers):
        self.input.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.input.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.input.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        self.input.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.input.on_key_release(symbol, modifiers)
