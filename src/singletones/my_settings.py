# /// script
# requires-python = ">=3.12"
# dependencies = [
# pygame-ce,
# src.ui.my_buttons
# ]
# [tool.uv]
# exclude-newer = "2025-02-12T00:00:00Z"
# ///


"""Файл, содержащий все параметры игры"""

import pygame

from src.ui.my_buttons import Button
from .my_routers import graphics_folder, game_folder

# Экран
DISPLAY_WIDTH = 1000
"""Ширина экрана"""
DISPLAY_HEIGHT = 800
"""высота экрана"""
FPS = 60
"""Частота кадров. Скорость игры, если не включать пропуск кадров"""
frame_skip = False
"""Включение пропуска кадров для одинаковой скорости игры при любой частоте кадров"""


GAME_STATES: list[str] = ["intro", "level", "settings"]
"""Возможные состояния игры 

intro[0] - начальная заставка,
level[1] - игра,
settings[2] - это настройки, туда можно попасть из любого состояния игры
"""

GAME_CAPTION = 'top down'
camera_centered = True
"""Камера по центру"""
start_camera = True
"""Позволяет в первый раз выравнивать камеру, после переключения"""
full_screen = True
"""Полноэкранный режим"""

offset = pygame.Vector2()
"""Смещение экрана игры. Для того, 
чтобы экран и персонаж могли перемещаться не только в пределах экрана, 
но и на любое расстояние необходимо смещать камеру и персонажа относительно нулевых координат."""

TILE_SIZE = 64
"""Размер плитки в пикселях"""
HITBOX_OFFSET = {
    'player': -100,
    'object': -60,
    'grass': -20,
    'invisible': 0}
"""Смещение хитбокса. Позволяет сделать хитбокс меньше, чем спрайт"""

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = f'{graphics_folder}/font/joystix.ttf'
UI_FONT_SIZE = 18

UI_PALETTE = {"settings_bg": "#443c4c",  # фон меню настроек
              "buttons_idle": "#7557a3",  # фон кнопок по умолчанию
              "pressed_bt": "#d1b1fa",  # фон включенных параметров (нажатых кнопок)
              "pointed_bt": "#8f5cf7",  # фон кнопки при наведении на нее мышки
              "buttons_shadow": "#644594",  # тени, отбрасываемые кнопками
              "hp_color": "#990000",  # цвет полоски здоровья
              "mana_color": "#071bad",  # цвет полоски маны, энергии
              "text_color": "#e2b651",  # цвет текста
              "Deep Maroon": "#820202",  #
              "gray": "#444444	",  #
              "title_screen": "#14134c",  #
              "ui_bar_border": "#111111",  # цвет краев полоски ХП
              "ui_bar_bg": "#222222",  # цвет пустой полоски ХП
              "ui_text": "#EEEEEE",
              "black": "#000000"}
"""Палитра цветов, используемая в интерфейсе"""

mouse_x, mouse_y = 0, 0
"""Положение мышки на экране"""

# Инвентарь
STAT_POS_X = 50
UI_HEIGHT = 100
INV_TILE_SIZE = 48
"""Размер ячейки инвентаря"""

is_armored = False
"""Узнать, экипировано ли оружие"""
armored_weapon = None
""""Экземпляр экипированного оружия"""
visible_sprites = None

sounds_ = True
angle = 0


def audio_settings():
    global sounds_
    if sounds_:
        pygame.mixer.unpause()
        sounds_ = False
    else:
        pygame.mixer.pause()
        sounds_ = True


class Settings:
    """Настройки, которые можно будет изменять в игре"""

    def __init__(self, game_state, fullscreen):
        self.game_state = game_state
        """Доступ к экземпляру класса состояний игры"""
        self.fullscreen = fullscreen
        self.display_surface = pygame.display.get_surface()
        """Получает текущую поверхность дисплея"""
        self.gui_font = pygame.font.Font(None, 30)
        """Шрифт интерфейса"""
        self.grab_cursor: bool = True
        """Курсор заблокирован"""
        pygame.event.set_grab(self.grab_cursor)  # Блокирует перемещение мыши за границу экрана
        self.button_ = {"Color scheme 1": {"top": '#6f6f6f', "bottom": '#0e0e0e', "collide": '#ebebeb'},
                        "Color scheme 2": {"top": '#c07c00', "bottom": '#513705', "collide": '#faa200'},
                        "Button 1": (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 300),
                        "Button 2": (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 240),
                        "Button 3": (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 180),
                        "Button 4": (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 120),
                        "Button 5": (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 60),
                        "Button 6": (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2),
                        "Button 7": (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 60),
                        "Button 8": (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 120),
                        "Button width": 400,
                        "Button height": 50
                        }
        """Словарь, содержащий: положение кнопок на экране, их размеры, цветовые схемы"""
        self.button_music = Button('Музыка',
                                   self.button_["Button width"], self.button_["Button height"],
                                   self.button_['Button 1'], self.gui_font, 6,
                                   top_color=self.button_["Color scheme 1"]["top"],
                                   bottom_color=self.button_["Color scheme 1"]['bottom'],
                                   collide_color=self.button_["Color scheme 1"]['collide'])
        self.button_fullscreen = Button('Полноэкранный режим',
                                        self.button_["Button width"], self.button_["Button height"],
                                        self.button_['Button 2'], self.gui_font, 6,
                                        top_color=self.button_["Color scheme 1"]['top'],
                                        bottom_color=self.button_["Color scheme 1"]['bottom'],
                                        collide_color=self.button_["Color scheme 1"]['collide'])
        self.button_grab = Button('Блокировка курсора',
                                  self.button_["Button width"], self.button_["Button height"],
                                  self.button_['Button 3'], self.gui_font, 6,
                                  top_color=self.button_["Color scheme 1"]['top'],
                                  bottom_color=self.button_["Color scheme 1"]['bottom'],
                                  collide_color=self.button_["Color scheme 1"]['collide'])
        self.button_4 = Button('НИЧЕГО',
                               self.button_["Button width"], self.button_["Button height"],
                               self.button_['Button 4'], self.gui_font, 6,
                               top_color=self.button_["Color scheme 1"]['top'],
                               bottom_color=self.button_["Color scheme 1"]['bottom'],
                               collide_color=self.button_["Color scheme 1"]['collide'])
        self.button_5 = Button('НИЧЕГО',
                               self.button_["Button width"], self.button_["Button height"],
                               self.button_['Button 5'], self.gui_font, 6,
                               top_color=self.button_["Color scheme 1"]['top'],
                               bottom_color=self.button_["Color scheme 1"]['bottom'],
                               collide_color=self.button_["Color scheme 1"]['collide'])
        self.button_6 = Button('В главное меню',
                               self.button_["Button width"], self.button_["Button height"],
                               self.button_['Button 6'], self.gui_font, 6,
                               top_color=self.button_["Color scheme 1"]['top'],
                               bottom_color=self.button_["Color scheme 1"]['bottom'],
                               collide_color=self.button_["Color scheme 1"]['collide'])
        self.button_back = Button(f'Вернуться',
                                  self.button_["Button width"], self.button_["Button height"],
                                  self.button_['Button 7'], self.gui_font, 6,
                                  top_color=self.button_["Color scheme 1"]['top'],
                                  bottom_color=self.button_["Color scheme 1"]['bottom'],
                                  collide_color=self.button_["Color scheme 1"]['collide'])
        self.button_exit = Button('Выход',
                                  self.button_["Button width"], self.button_["Button height"],
                                  self.button_['Button 8'], self.gui_font, 6,
                                  top_color=self.button_["Color scheme 1"]['top'],
                                  bottom_color=self.button_["Color scheme 1"]['bottom'],
                                  collide_color=self.button_["Color scheme 1"]['collide'])

    def settings_cursor(self):
        """Переключение блокировки мыши в окне"""
        if self.grab_cursor:
            self.grab_cursor = False
        else:
            self.grab_cursor = True
        pygame.event.set_grab(self.grab_cursor)

    def run(self, dt=None):
        # Цвет экрана
        self.display_surface.fill(UI_PALETTE["settings_bg"])
        # Кнопки
        self.button_music.draw()
        self.button_music.check_mouse_click(audio_settings)
        self.button_fullscreen.draw()
        self.button_fullscreen.check_mouse_click(function=lambda: self.fullscreen.run())
        self.button_grab.draw()
        self.button_grab.check_mouse_click(self.settings_cursor)
        self.button_4.draw()
        self.button_4.check_mouse_click()
        self.button_5.draw()
        self.button_5.check_mouse_click()
        self.button_6.draw()
        self.button_6.check_mouse_click(
            function=lambda: self.game_state.set_state('intro'))
        self.button_back.draw()
        self.button_back.check_mouse_click(
            function=lambda: self.game_state.set_state(self.game_state.get_previous_state()))
        self.button_exit.draw()
        self.button_exit.check_mouse_click(function=game_exit)

def game_exit() -> None:
    pygame.quit()
    # sys.exit()
    
if __name__ == '__main__':
    pass
