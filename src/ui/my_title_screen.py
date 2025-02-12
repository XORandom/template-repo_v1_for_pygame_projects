# /// script
# requires-python = ">=3.12"
# dependencies = [pygame-ce]

# [tool.uv]
# exclude-newer = "2025-02-12T00:00:00Z"
# ///

"""Главный экран до начала игры"""

import pygame
from .my_buttons import Button

class TitleScreen:
    def __init__(self, 
                 game_state,
                 title_screen_color = "#14134c"
                 ):
        self.game_state = game_state
        """Доступ к экземпляру класса состояний игры"""
        self.display_surface = pygame.display.get_surface()
        """Получает текущую поверхность дисплея"""
        self.gui_font = pygame.font.Font(None, 30)
        """Шрифт интерфейса"""
        self.title_screen_color = title_screen_color
        """Цвет фона главного экрана"""
        self.button_start = Button('Начать игру', 400, 80,
                                   (pygame.display.get_window_size().x // 2, pygame.display.get_window_size().y // 2 - 100), self.gui_font, 6)
        self.button_settings = Button('Настройки', 400, 80,
                                      (pygame.display.get_window_size().x // 2, pygame.display.get_window_size().y // 2), self.gui_font, 6)
        self.button_exit = Button('Выход', 400, 80,
                                  (pygame.display.get_window_size().x // 2, pygame.display.get_window_size().y // 2 + 100), self.gui_font, 6)

    def run(self, dt=None):
        # Цвет экрана
        self.display_surface.fill(self.title_screen_color)
        # Кнопки
        self.button_start.draw()
        self.button_start.check_mouse_click(function=lambda: self.game_state.set_state('level'))
        self.button_settings.draw()
        self.button_settings.check_mouse_click(function=lambda: self.game_state.set_state('settings'))
        self.button_exit.draw()
        self.button_exit.check_mouse_click(function=game_exit)

def game_exit() -> None:
    pygame.quit()
    # sys.exit()

if __name__ == '__main__':
    pass
