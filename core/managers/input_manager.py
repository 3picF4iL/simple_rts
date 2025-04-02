import arcade

class InputManager:
    def __init__(self, gui_manager, selection_manager, unit_manager, building_manager):
        self.gui = gui_manager
        self.selection = selection_manager
        self.units = unit_manager
        self.buildings = building_manager
        self._mouse_down = False

    def on_mouse_press(self, x, y, button, modifiers):
        self._mouse_down = True
        if self.gui.is_mouse_over_gui(x, y):
            return self.gui.handle_mouse_press(x, y, button)

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.selection.start_selection(x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.units.command_move(self.selection.selected_objects, x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        self._mouse_down = False
        if self.gui.is_mouse_over_gui(x, y):
            if not self.selection.selecting:
                return self.gui.handle_mouse_release(x, y, button)

        if button == arcade.MOUSE_BUTTON_LEFT:
            dx = abs(self.selection.start_x - x)
            dy = abs(self.selection.start_y - y)

            if dx < 5 and dy < 5:
                self.selection.select_by_click(
                    self.units.get_units(),
                    self.buildings.get_buildings(),
                    x, y
                )
            else:
                self.selection.select_by_box(
                    self.units.get_units(),
                    self.selection.start_x,
                    self.selection.start_y,
                    x, y
                )

            self.gui.set_active_objects(self.selection.selected_objects)
            self.selection.selecting = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.gui.handle_mouse_motion(x, y, dx, dy)
        if self._mouse_down:
            self.selection.update_selection(x, y)
