class State:
    def __init__(self, game):
        self.game = game
        self.utils = game.utils

    def cleanup(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass
