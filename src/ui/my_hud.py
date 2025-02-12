# /// script
# requires-python = ">=3.12"
# dependencies = [pygame-ce, src.singletones.my_settings]
# [tool.uv]
# exclude-newer = "2025-02-12T00:00:00Z"
# ///



"""Графический интерфейс показывающий характеристики для игрока"""

import pygame
from src.singletones import my_settings


class HUD:
    """Класс для отображения HUD на экране"""
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        """Поверхность для отображения графики"""

        self.font = pygame.font.Font(my_settings.UI_FONT, my_settings.UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, my_settings.HEALTH_BAR_WIDTH, my_settings.BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, my_settings.ENERGY_BAR_WIDTH, my_settings.BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, bar_color):
        """Рисует полоску хп, маны и т.д"""
        # draw bg
        pygame.draw.rect(self.display_surface, my_settings.UI_PALETTE["ui_bar_bg"], bg_rect)

        if current < 0:
            current = 0
        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, bar_color, current_rect)
        pygame.draw.rect(self.display_surface, my_settings.UI_PALETTE["ui_bar_border"], bg_rect, 3)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, my_settings.UI_PALETTE["hp_color"])
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, my_settings.UI_PALETTE["mana_color"])

if __name__ == '__main__':
    pass
