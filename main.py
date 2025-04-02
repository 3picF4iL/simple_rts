import arcade
from core.game_view import GameView
from utils.i18n import init_translator


def main():
    init_translator("pl")

    window = arcade.Window(1440, 900, "RTS")
    view = GameView()
    window.show_view(view)
    window.set_location(100, 50)
    arcade.run()

if __name__ == "__main__":
    main()
