import arcade

class SelectionManager:
    def __init__(self):
        self.selecting = False
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.selected_objects = []

    def start_selection(self, x, y):
        self.selecting = True
        self.start_x = self.end_x = x
        self.start_y = self.end_y = y

    def update_selection(self, x, y):
        self.end_x = x
        self.end_y = y

    def select_by_box(self, units, x1, y1, x2, y2):
        self.clear_selection()
        for unit in units:
            if self._point_in_box(unit.center_x, unit.center_y, x1, y1, x2, y2):
                unit.selected = True
                self.selected_objects.append(unit)
            else:
                unit.selected = False
        self.selecting = False

    def select_by_click(self, units, buildings, x, y):
        self.clear_selection()

        # Priority: units
        for unit in units:
            if unit.collides_with_point((x, y)):
                unit.selected = True
                self.selected_objects.append(unit)
                self._deselect_all(buildings)
                return
            else:
                unit.selected = False

        # If no unit selected by click, check buildings
        for building in buildings:
            if building.collides_with_point((x, y)):
                building.selected = True
                self.selected_objects.append(building)
            else:
                building.selected = False

        self.selecting = False

    def clear_selection(self):
        for s_obj in self.selected_objects:
            s_obj.selected = False
        self.selected_objects.clear()

    def _deselect_all(self, objects):
        for obj in objects:
            obj.selected = False

    def get_selected(self):
        return self.selected_objects

    def _point_in_box(self, cx, cy, x1, y1, x2, y2):
        return min(x1, x2) < cx < max(x1, x2) and min(y1, y2) < cy < max(y1, y2)

    def draw(self):
        if self.selecting:
            left = min(self.start_x, self.end_x)
            right = max(self.start_x, self.end_x)
            bottom = min(self.start_y, self.end_y)
            top = max(self.start_y, self.end_y)
            arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.YELLOW, 2)

