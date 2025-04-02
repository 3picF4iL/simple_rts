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

    def on_mouse_press(self, x: float, y: float, button: int):
        pass

    def on_mouse_release(self, x: float, y: float, button: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.hovered = self.contains_point(x, y)


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
    def __init__(self, x, y, text: str):
        super().__init__(x, y, width=0, height=0)
        self.text_obj = arcade.Text(
            text,
            x,
            y,
            arcade.color.WHITE,
            12,
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

        try:
            for obj in objects:
                if hasattr(obj, "get_info"):
                    for idx, line in enumerate(obj.get_info()):
                        label = GUILabel(10, 50 + idx * 20, line)
                        self.active_info_labels.append(label)

                if hasattr(obj, "get_actions"):
                    for i, action in enumerate(obj.get_actions()):
                        button = GUIButton(
                            x=10 + i * 170,
                            y=10,
                            width=160,
                            height=30,
                            label=action["label"],
                            action=lambda a=action: game_controller.perform_action(a["action"], obj)
                        )
                        self.action_buttons.append(button)
        except Exception as e:
            print("[HUDLayout] Active elements update error:", e)

    def clear_active_elements(self):
        self.active_info_labels.clear()
        self.action_buttons.clear()

    def draw(self):
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            self.window.height - self.top_bar_height,
            self.window.height,
            arcade.color.DARK_SLATE_GRAY
        )
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width,
            0, self.bottom_bar_height,
            arcade.color.DIM_GRAY
        )

        for label in self.resource_name_labels:
            label.draw()
        for label in self.resource_value_labels.values():
            label.draw()
        for label in self.active_info_labels:
            label.draw()
        for button in self.action_buttons:
            button.draw()

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
        self.hud.set_active_elements(objects, self.game_controller)

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

    def update(self, dt: float):
        for element in self.elements:
            element.update(dt)

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
        for element in reversed(self.elements):
            if element.visible and element.contains_point(x, y):
                if element.on_mouse_release(x, y, button):
                    return True
        return False

    def handle_mouse_motion(self, x, y, dx, dy):
        for element in self.elements:
            element.on_mouse_motion(x, y, dx, dy)

    def is_mouse_over_gui(self, x, y):
        return (
            self.hud.is_in_hud_area(x, y) or
            any(e.contains_point(x, y) for e in self.elements if e.visible)
        )
