import arcade
from core.game_view import GameView

def main():
    window = arcade.Window(1280, 720, "RTS Etap 1")
    view = GameView()
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
