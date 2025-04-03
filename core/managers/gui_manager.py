import arcade
from utils.i18n import t
from typing import Optional, Callable

class GUIElement:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.hovered = False

    def draw(self):
        pass

    def update(self, dt: float):
        pass

    def contains_point(self, x: float, y: float) -> bool:
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


class GUIButton(GUIElement):
    def __init__(self, x, y, width, height, label: str, action: Callable):
        super().__init__(x, y, width, height)
        self.label = label
        self.action = action
        self.pressed = False
        self.text_obj = arcade.Text(
            label,
            x + 8,
            y + height / 2,
            arcade.color.YELLOW,
            10,
            anchor_y="center"
        )

    def draw(self):
        if not self.visible:
            return

        if self.pressed:
            arcade.draw_lrbt_rectangle_filled(
                self.x, self.x + self.width,
                self.y, self.y + self.height,
                arcade.color.GRAY
            )
        elif self.hovered:
            arcade.draw_lrbt_rectangle_filled(
                self.x, self.x + self.width,
                self.y, self.y + self.height,
                arcade.color.DARK_GRAY
            )

        arcade.draw_lrbt_rectangle_outline(
            self.x, self.x + self.width,
            self.y, self.y + self.height,
            arcade.color.YELLOW, 2
        )

        self.text_obj.draw()

    def on_mouse_press(self, x: float, y: float, button: int):
        if button == arcade.MOUSE_BUTTON_LEFT and self.contains_point(x, y):
            self.pressed = True
            return True
        return False

    def on_mouse_release(self, x: float, y: float, button: int):
        if self.pressed and button == arcade.MOUSE_BUTTON_LEFT and self.contains_point(x, y):
            self.pressed = False
            self.action()
            return True
        self.pressed = False
        return False


class GUILabel(GUIElement):
    def __init__(self, x, y, text: str, size: int = 12):
        super().__init__(x, y, width=0, height=0)
        self.text_obj = arcade.Text(
            text,
            x,
            y,
            arcade.color.WHITE,
            size,
            anchor_y="bottom"
        )

    def draw(self):
        if self.visible:
            self.text_obj.draw()

    def set_text(self, new_text: str):
        self.text_obj.text = new_text


class HUDLayout:
    def __init__(self, window, top_bar_height=30, bottom_bar_height=100):
        self.window = window
        self.top_bar_height = top_bar_height
        self.bottom_bar_height = bottom_bar_height
        self.resources = ["wood", "food", "gold", "stone"]
        self.resource_name_labels: list[GUILabel] = []
        self.resource_value_labels: dict[str, GUILabel] = {}
        self.active_info_labels: list[GUILabel] = []
        self.action_buttons: list[GUIButton] = []
        self.queue_labels: list[GUILabel] = []
        self._init_resource_labels()

    def _init_resource_labels(self):
        spacing = self.window.width // len(self.resources)
        for i, res in enumerate(self.resources):
            name_label = GUILabel(10 + i * spacing, self.window.height - self.top_bar_height + 6, t(res))
            value_label = GUILabel(70 + i * spacing, self.window.height - self.top_bar_height + 6, "0")
            self.resource_name_labels.append(name_label)
            self.resource_value_labels[res] = value_label

    def set_resource_value(self, resource: str, value: int):
        if resource in self.resource_value_labels:
            self.resource_value_labels[resource].set_text(str(value))

    def set_active_elements(self, objects, game_controller):
        self.active_info_labels.clear()
        self.action_buttons.clear()

        for obj in objects or []:
            self._add_info_labels(obj)
            self._add_action_buttons(obj, game_controller)


    def _add_info_labels(self, obj):
        if hasattr(obj, "get_info"):
            lines = obj.get_info()
            for idx, line in enumerate(reversed(lines)):
                font_size = 12 if idx != 0 else 8
                label = GUILabel(10, 50 + idx * 20, line, size=font_size)
                self.active_info_labels.append(label)

    def _add_action_buttons(self, obj, game_controller):
        if not hasattr(obj, "production_options"):
            return

        for i, option in enumerate(obj.production_options):
            cls = game_controller.get_entity_class(option)
            if not cls:
                continue

            button = GUIButton(
                x=10 + i * 170,
                y=10,
                width=160,
                height=30,
                label=cls.NAME,
                action=lambda c=cls: game_controller.handle_production_click(c, obj)
            )
            self.action_buttons.append(button)

    def add_queue_lines(self, lines: list[str]):
        self.queue_labels.clear()
        for idx, line in enumerate(lines):
            label = GUILabel(
                x=self.window.width // 2 - 80,
                y=10 + idx * 16,
                text=line
            )
            self.queue_labels.append(label)

    def clear_active_elements(self):
        self.active_info_labels.clear()
        self.action_buttons.clear()
        self.queue_labels.clear()

    def _draw_top_bar_bg(self):
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            self.window.height - self.top_bar_height,
            self.window.height,
            arcade.color.DARK_SLATE_GRAY
        )

    def _draw_bottom_bar_bg(self):
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            0, self.bottom_bar_height,
            arcade.color.DIM_GRAY
        )

    def draw(self):
        self._draw_top_bar_bg()
        self._draw_bottom_bar_bg()

        for group in [
            self.resource_name_labels,
            self.resource_value_labels.values(),
            self.action_buttons,
            self.active_info_labels,
            self.queue_labels
        ]:
            for item in group:
                item.draw()

    def is_in_hud_area(self, x, y):
        return y >= self.window.height - self.top_bar_height or y <= self.bottom_bar_height


class GUIManager:
    def __init__(self, window, game_controller):
        self.window = window
        self.elements: list[GUIElement] = []
        self.hud = HUDLayout(window)
        self.active_objects: list = []
        self.game_controller = game_controller

    def add(self, element: GUIElement):
        self.elements.append(element)

    def clear_elements(self):
        self.elements.clear()
        self.hud.clear_active_elements()

    def set_active_objects(self, objects):
        self.active_objects = objects
        if objects:
            self.hud.set_active_elements(objects, self.game_controller)
        else:
            self.hud.clear_active_elements()

    def set_click_info(self, text):
        # Temporary debug method
        print(text)

    def clear_active_objects(self):
        self.active_objects.clear()
        self.hud.clear_active_elements()

    def draw(self):
        self.hud.draw()
        for element in self.elements:
            element.draw()

    def update_active_obj_queue(self):
        if self.active_objects:
            obj = self.active_objects[0]
            if hasattr(obj, "get_production_queue_lines"):
                lines = obj.get_production_queue_lines()
                self.hud.add_queue_lines(lines)

    def update_resources(self):
        for resource, value in self.game_controller.resource_manager.get_all().items():
            self.hud.set_resource_value(resource, value)

    def update(self, dt: float):
        for element in self.elements:
            element.update(dt)

        self.update_resources()
        self.update_active_obj_queue()

    def handle_mouse_press(self, x, y, button):
        for button_element in reversed(self.hud.action_buttons):
            if button_element.visible and button_element.contains_point(x, y):
                if button_element.on_mouse_press(x, y, button):
                    return True
        for element in reversed(self.elements):
            if element.visible and element.contains_point(x, y):
                if element.on_mouse_press(x, y, button):
                    return True
        return False

    def handle_mouse_release(self, x, y, button):
        for button_element in reversed(self.hud.action_buttons):
            if button_element.visible and button_element.contains_point(x, y):
                if button_element.on_mouse_release(x, y, button):
                    return True
        for element in self.elements:
            if element.visible and element.contains_point(x, y):
                if element.on_mouse_release(x, y, button):
                    return True
        return False

    def is_mouse_over_gui(self, x, y):
        return (
            self.hud.is_in_hud_area(x, y) or
            any(e.contains_point(x, y) for e in self.elements if e.visible)
        )
