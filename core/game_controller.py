class GameController:
    def __init__(self, unit_manager, building_manager, gui_manager):
        self.unit_manager = unit_manager
        self.building_manager = building_manager
        self.gui_manager = gui_manager

    def perform_action(self, action_dict, source_obj):
        if action_dict["type"] == "create_unit":
            unit_cls = self.unit_manager.unit_map[action_dict.get("unit_type")]
            source_obj.add_to_queue(unit_cls)
            self.gui_manager.set_click_info(f"Added to queue: {unit_cls.NAME}")

    def build_gui_for(self, selected_object):
        self.gui_manager.clear_elements()
        self.gui_manager.set_active_objects([selected_object])
