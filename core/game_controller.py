from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductionRequest:
    name: str
    type: str
    cost: dict
    source: Optional[object]


class GameController:
    def __init__(self, unit_manager, building_manager, resource_manager, gui_manager, build_mode_manager, entity_factory):
        self.unit_manager = unit_manager
        self.building_manager = building_manager
        self.gui_manager = gui_manager
        self.resource_manager = resource_manager
        self.build_mode_manager = build_mode_manager
        self.factory = entity_factory
        self.pending_request: Optional[ProductionRequest] = None

    def handle_production_click(self, entity_name: str, source_obj):
        type = self.factory.get_type(entity_name)
        cost = self.factory.get_cost(entity_name)

        self.pending_request = ProductionRequest(
            name=entity_name,
            type=type,
            cost=cost,
            source=source_obj
        )

        self.confirm_production()

    def confirm_production(self):
        req = self.pending_request
        if not req:
            return

        if not self.resource_manager.can_afford(req.cost):
            self.gui_manager.set_click_info(f"Not enough resources for {req.name}")
            self.pending_request = None
            return
        
        print(req)

        if "unit" in req.type:
            self.resource_manager.pay(req.cost)
            req.source.add_to_queue(req.name)
            #self.gui_manager.set_click_info(f"Queued: {req.name}")
            self.pending_request = None

        elif "building" in req.type:
            self.set_build_mode(req.name)
            #self.gui_manager.set_click_info(f"Enter build mode: {req.name}")

    def try_place_building(self):
        req = self.pending_request
        if not req or "building" not in req.type:
            return

        if not self.resource_manager.can_afford(req.cost):
            self.gui_manager.set_click_info(f"Not enough resources to place {req.name}")
            return

        self.resource_manager.pay(req.cost)
        self.build_mode_manager.place()
        #self.gui_manager.set_click_info(f"Placed: {req.name}")
        self.pending_request = None

    def set_build_mode(self, entity_name):
        self.build_mode_manager.start(entity_name)

    def build_gui_for(self, selected_object):
        self.gui_manager.clear_elements()
        self.gui_manager.set_active_objects([selected_object])
