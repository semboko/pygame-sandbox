from pygame.surface import Surface


class AbstractMenu:
    def __init__(self):
        self.active = False

        # Buttons, inputs...

    def render(self, display: Surface):
        # For button in buttons, inputs:
        #   button.render(display)
        pass
