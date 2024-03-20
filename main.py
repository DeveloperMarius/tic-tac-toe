#!/usr/bin/env python3

import pygame
from src.windows.window_manager import WindowManager
from src.windows.main_menu_window import MainMenuWindow


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        WindowManager.get_instance().activeWindow = MainMenuWindow()
        self.run()

    def run(self):
        while self.running:
            self.handleEvents()
            self.render()
            self.clock.tick(30)  # limits FPS to 60
        pygame.quit()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                WindowManager.get_instance().activeWindow.handleEvent(event)

    def render(self):
        if WindowManager.get_instance().activeWindow is None:
            print('Active window is None')
            return
        self.window.fill((7, 12, 23))
        WindowManager.get_instance().activeWindow.draw(self.window)
        pygame.display.flip()


if __name__ == "__main__":
    Main()
