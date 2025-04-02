from utils.i18n import t


class Entity:
    NAME = "Name placeholder"
    DESCRIPTION = "Description placeholder"

    def __init__(self):
        pass

    def get_info(self):
        return [t(f"{self.name}"), t(f"{self.description}")]

    @property
    def name(self):
        return self.NAME

    @property
    def description(self):
        return self.DESCRIPTION
