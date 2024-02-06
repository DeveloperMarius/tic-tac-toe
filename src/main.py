# Example file showing a basic pygame "game loop"
import pygame
from window_manager import WindowManager
from windows.main_menu_window import MainMenuWindow

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
windowManager = WindowManager()
windowManager.activeWindow = MainMenuWindow()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            windowManager.activeWindow.handleEvent(event)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    windowManager.activeWindow.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
