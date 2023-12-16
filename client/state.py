class State:
    def __init__(self, game):
        self.game = game
        self.fonts = game.fonts

    def cleanup(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass
