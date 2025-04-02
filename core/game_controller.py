from core.managers.gui_manager import GUIButton, GUILabel

class GameController:
    def __init__(self, unit_manager, building_manager, gui_manager):
        self.unit_manager = unit_manager
        self.building_manager = building_manager
        self.gui_manager = gui_manager

    def perform_action(self, action: str, selected_object):
        if action == "create_unit":
            self._handle_create_unit(selected_object)

    def _handle_create_unit(self, selected_object):
        if not selected_object:
            self.gui_manager.set_click_info("[ERR] No building selected.")
            return

        if not hasattr(selected_object, "center_x") or not hasattr(selected_object, "center_y"):
            self.gui_manager.set_click_info("[ERR] Invalid object.")
            return

        spawn_x = selected_object.center_x + selected_object.width // 2 + 20
        spawn_y = selected_object.center_y

        self.unit_manager.spawn_unit(spawn_x, spawn_y)
        self.gui_manager.set_click_info("Unit created.")

    def build_gui_for(self, selected_object):
        self.gui_manager.clear_elements()

        self.gui_manager.add(GUILabel(
            x=10,
            y=80,
            text=selected_object.get_hover_info()
        ))

        for idx, action in enumerate(selected_object.get_actions()):
            self.gui_manager.add(GUIButton(
                x=10 + idx * 170,
                y=10,
                width=160,
                height=30,
                label=action["label"],
                action=lambda act=action: self.perform_action(act["action"], selected_object)
            ))
