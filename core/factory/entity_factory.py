class EntityFactory:
    def __init__(self, unit_defs, building_defs):
        self.unit_defs = unit_defs
        self.building_defs = building_defs

    def create_unit(self, name, x, y):
        config = self.unit_defs.get(name)
        if not config:
            raise Exception(f"Unknown unit: {name}")
        from core.entities.unit import Unit
        return Unit(x, y, config)

    def create_building(self, name, x, y):
        config = self.building_defs.get(name)
        if not config:
            raise Exception(f"Unknown building: {name}")
        from core.entities.building import Building
        return Building(x, y, config)

    def get_definition(self, name):
        return self.unit_defs.get(name) or self.building_defs.get(name)

    def get_type(self, name):
        definition = self.get_definition(name)
        return definition.get("type") if definition else None

    def get_cost(self, name):
        definition = self.get_definition(name)
        return definition.get("cost", {}) if definition else {}

    def get_creation_time(self, name):
        definition = self.get_definition(name)
        return definition.get("creation_time", 1.0) if definition else 1.0
