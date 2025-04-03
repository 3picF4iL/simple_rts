from utils.i18n import t


class Entity:
    NAME = "Name placeholder"
    DESCRIPTION = "Description placeholder"
    ENTITY_TYPE = ''

    def __init__(self):
        self.production_options = []

    def get_info(self):
        return [t(f"{self.name}"), t(f"{self.description}")]

    @property
    def name(self):
        return self.NAME

    @property
    def description(self):
        return self.DESCRIPTION
