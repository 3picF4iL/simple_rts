import arcade
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
        arcade.draw_text(
            self.label,
            self.x + 8,
            self.y + self.height / 2 - 7,
            arcade.color.YELLOW,
            12,
            anchor_y="center"
        )

    def on_mouse_press(self, x: float, y: float, button: int):
        if button == arcade.MOUSE_BUTTON_LEFT and self.contains_point(x, y):
            self.pressed = True
            return True
        return False

    def on_mouse_release(self, x: float, y: float, button: int):
        if self.pressed and button == arcade.MOUSE_BUTTON_LEFT and self.contains_point(x, y):
            self.pressed = False
            self.action()  # wywołanie akcji
            return True
        self.pressed = False
        return False


class GUILabel(GUIElement):
    def __init__(self, x, y, text: str):
        super().__init__(x, y, width=0, height=0)
        self.text = text

    def draw(self):
        if self.visible:
            arcade.draw_text(self.text, self.x, self.y, arcade.color.WHITE, 14)


class HUDLayout:
    def __init__(self, window, top_bar_height=30, bottom_bar_height=100):
        self.window = window
        self.top_bar_height = top_bar_height
        self.bottom_bar_height = bottom_bar_height

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

    def is_in_hud_area(self, x, y):
        return y >= self.window.height - self.top_bar_height or y <= self.bottom_bar_height


class GUIManager:
    def __init__(self, window):
        self.window = window
        self.elements: list[GUIElement] = []
        self.hud = HUDLayout(window)

    def add(self, element: GUIElement):
        self.elements.append(element)

    def clear_elements(self):
        self.elements.clear()

    def draw(self):
        self.hud.draw()
        for element in self.elements:
            element.draw()

    def update(self, dt: float):
        for element in self.elements:
            element.update(dt)

    def handle_mouse_press(self, x, y, button):
        for element in reversed(self.elements):
            if element.visible and element.contains_point(x, y):
                if element.on_mouse_press(x, y, button):
                    return True
        return False

    def handle_mouse_release(self, x, y, button):
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
