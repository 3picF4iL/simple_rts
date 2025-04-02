from core.managers.gui_manager import GUIButton, GUILabel

class GameController:
    def __init__(self, unit_manager, building_manager, gui_manager):
        self.unit_manager = unit_manager
        self.building_manager = building_manager
        self.gui_manager = gui_manager

    def perform_action(self, action_dict, source_obj):
        if action_dict["type"] == "create_unit":
            unit_type = action_dict["unit_type"]
            spawn_x = source_obj.center_x + 100
            spawn_y = source_obj.center_y
            self.unit_manager.spawn_unit(unit_type, spawn_x, spawn_y)
            self.gui_manager.set_click_info(f"Created: {unit_type}")

    def build_gui_for(self, selected_object):
        self.gui_manager.clear_elements()
        self.gui_manager.set_active_objects([selected_object])
