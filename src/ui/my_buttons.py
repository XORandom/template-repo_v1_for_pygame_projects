# /// script
# requires-python = ">=3.12"
# dependencies = [pygame-ce]

# [tool.uv]
# exclude-newer = "2025-02-12T00:00:00Z"
# ///

import pygame

class Button:
    """Базовый класс для всех кнопок"""

    def __init__(self, text: str, 
                 width: int,                # Ширина кнопки
                 height: int,               # Высота кнопки
                 pos: tuple,                # Координаты кнопки
                 gui_font,                  # Шрифт, используемый в тексте на кнопке
                 elevation: int,            # Высота кнопки
                 top_color ='#c07c00',       # Цвет верхней поверхности кнопки
                 bottom_color='#c07c00',    # Цвет нижней поверхности кнопки
                 hover_color='#c07c00',     # Цвет кнопки при наведении мыши
                 font_color='#ffffff',      # Цвет текста на кнопке
                 ):
        self.pressed = False
        """Кнопка нажата"""
        self.elevation = elevation
        """Высота кнопки"""
        self.dynamic_elevation = self.elevation
        """Текущая высота кнопки"""
        self.original_pos_y = pos[1]
        """Исходное положение кнопки до клика. 
        Кнопка перемещается вниз при клике, нам надо знать, где она была до этого"""

        self.display_surface = pygame.display.get_surface()
        """Получает текущую поверхность дисплея"""
        self.top_rect = pygame.Rect(pos, (width, height))
        """Прямоугольник верхней части кнопки Rect(x, y, w, h). Отрисован в левой верхней точке координат"""
        self.middle_rect = pygame.Rect((self.top_rect.x, self.top_rect.y - self.elevation), (width, height-self.elevation))
        """Та часть кнопки, на которую можно нажать мышкой. 
        Предотвращает дергание кнопки вверх-вниз при наведении мышки на верхнюю часть кнопки"""
        self.top_color = top_color
        """Цвет верхней поверхности кнопки"""
        self.hover_color = hover_color
        """Цвет верхней поверхности кнопки после наведения мышки"""
        self.prev_top_color = self.top_color
        """Предыдущий цвет кнопки"""
        self.bottom_rect = pygame.Rect(pos, (width, height))
        """Нижняя часть кнопки"""
        self.bottom_color = bottom_color
        """Цвет нижней поверхности кнопки"""
        self.text_surf = gui_font.render(text, True, font_color)
        """Отображение текста"""
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        """Расположение текста на кнопке"""

    def draw(self):
        self.top_rect.y = self.original_pos_y - self.dynamic_elevation
        """Поднимаем кнопку наверх"""
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.display_surface, self.bottom_color, self.bottom_rect, border_radius=14)
        pygame.draw.rect(self.display_surface, self.top_color, self.top_rect, border_radius=14)
        self.display_surface.blit(self.text_surf, self.text_rect)

    def check_mouse_click(self, function=lambda: print('click')):
        mouse_pos = pygame.mouse.get_pos()

        if self.middle_rect.collidepoint(mouse_pos):
            self.top_color = self.hover_color
            if pygame.mouse.get_pressed()[0]:  # ЛКМ
                self.dynamic_elevation = 0  # Опускаем кнопку при нажатии
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:  # Выполняется после нажатия кнопки мыши
                    function()  # Содержит функцию, вызываемую при нажатии
                    self.pressed = False
        else:
            # Возвращаем исходное состояние кнопки, как только ее покидает мышка
            self.dynamic_elevation = self.elevation
            self.pressed = False
            self.top_color = self.prev_top_color

if __name__ == '__main__':
    pass
