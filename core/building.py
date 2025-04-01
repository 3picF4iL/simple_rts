import arcade

class Building(arcade.Sprite):
    def __init__(self, x, y):
        texture = arcade.make_soft_square_texture(60, arcade.color.RED, 255)
        super().__init__(texture, center_x=x, center_y=y)

        self.selected = False

    def setup(self):
        pass
