class ResourceManager:
    def __init__(self):
        self.resources = {
            "wood": 500,
            "food": 300,
            "gold": 100,
            "stone": 200,
        }

    def get(self, resource: str) -> int:
        return self.resources.get(resource, 0)

    def set(self, resource: str, amount: int):
        self.resources[resource] = amount

    def add(self, resource: str, amount: int):
        self.resources[resource] = self.get(resource) + amount

    def subtract(self, resource: str, amount: int):
        self.resources[resource] = max(0, self.get(resource) - amount)

    def can_afford(self, cost: dict[str, int]) -> bool:
        return all(self.get(k) >= v for k, v in cost.items())

    def pay(self, cost: dict[str, int]):
        for k, v in cost.items():
            self.subtract(k, v)

    def get_all(self):
        return self.resources.copy()
