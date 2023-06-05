import pygame


class Button:
    def __init__(self, image, x, y, scale):
        self.height = image.get_height()
        self.width = image.get_width()
        self.image = pygame.transform.rotozoom(image, 0, scale)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.clicked = False

    def draw(self, surface):
        # True or False will be returned
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check if button was clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, self.rect)

        return action
