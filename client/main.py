import pygame

from states.menu import MenuState
from surfaces import Surfaces
from utils.path import get_icon_path
from utils.fonts import Fonts

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.SCREEN_SIZE = (1200, 700)
        self.GAME_SIZE = (1200, 700)

        self.main_canvas = pygame.Surface(self.GAME_SIZE)
        icon = pygame.image.load(get_icon_path())
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Kidang Tikus")

        self.clock = pygame.time.Clock()
        self.running = True

        self.surfaces = Surfaces(self)
        self.fonts = Fonts(self)

        self.states = []
        initialMenuState = MenuState(self)
        self.open_state(initialMenuState)

    def loop(self):
        while self.running:
            self.update()
            self.handle_events()
            self.render()
            self.clock.tick(60)

    def exit(self):
        pygame.quit()

    def states_copy(self):
        return self.states.copy()

    def handle_events(self):
        clicksInStep = 0
        states = self.states_copy()
        for event in pygame.event.get():
            # Update the window size
            if event.type == pygame.VIDEORESIZE:
                self.SCREEN_SIZE = event.size

            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.QUIT:
                self.running = False

            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
                              pygame.MOUSEMOTION]:  # Fix mouse position (if the screen is resized)
                event.pos = (event.pos[0] * self.GAME_SIZE[0] / self.SCREEN_SIZE[0],
                             event.pos[1] * self.GAME_SIZE[1] / self.SCREEN_SIZE[1])

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicksInStep += 1
                if clicksInStep > 1:  # Discard the clicks if multiple per step
                    continue

            # Dispatch across states
            for state in states:
                state.handle_event(event)

    def update(self):
        for state in self.states_copy():
            state.update()

    def render(self):
        self.main_canvas.fill((0, 0, 0))

        self.surfaces.render_surfaces()

        self.screen.blit(pygame.transform.scale(self.main_canvas, self.SCREEN_SIZE), (0, 0))
        pygame.display.flip()

    def open_state(self, state):
        self.states.append(state)

    def close_state(self, state):
        state.cleanup()
        self.states.remove(state)


if __name__ == "__main__":
    game = Game()
    game.loop()
    game.exit()
