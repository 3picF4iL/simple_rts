class GameController:
    def __init__(self, unit_manager, building_manager, resource_manager, gui_manager):
        self.unit_manager = unit_manager
        self.building_manager = building_manager
        self.gui_manager = gui_manager
        self.resource_manager = resource_manager

        self.build_mode = None

    def handle_production_click(self, entity_cls, source_obj):
        if entity_cls.ENTITY_TYPE == "unit":
            if self.can_afford(entity_cls):
                self.pay(entity_cls.COST)
                source_obj.add_to_queue(entity_cls)
        elif entity_cls.ENTITY_TYPE == "building":
            self.set_build_mode(entity_cls)

    def get_entity_class(self, name):
        return (
            self.unit_manager.units_map.get(name)
            or self.building_manager.buildings_map.get(name)
        )

    def __perform_action(self, action_dict, source_obj):
        # TODO: This method should be used for actions different than production
        # Disabling for now
        if action_dict["type"] == "create_unit":
            unit_cls = self.unit_manager.unit_map[action_dict.get("unit_type")]

            if self.can_afford(unit_cls):
                self.pay(unit_cls.COST)
                source_obj.add_to_queue(unit_cls)
                self.gui_manager.set_click_info(f"Added to queue: {unit_cls.NAME}")
            else:
                self.gui_manager.set_click_info(f"Not enough resources for {unit_cls.NAME}")

    def can_afford(self, unit_cls):
        return self.resource_manager.can_afford(unit_cls.COST)

    def pay(self, costs):
        self.resource_manager.pay(costs)

    def build_gui_for(self, selected_object):
        self.gui_manager.clear_elements()
        self.gui_manager.set_active_objects([selected_object])

    def set_build_mode(self, cls):
        print("Not implemented")
