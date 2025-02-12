# /// script
# requires-python = ">=3.12"
# dependencies = [pygame-ce, os.path, os.walk, csv.reader]
# [tool.uv]
# exclude-newer = "2025-02-12T00:00:00Z"
# ///


"""
Связывает пути файлов 
Для контроля над путями, загрузкой спрайтов,плиток
"""

import pygame
from os import path, walk
from csv import reader


game_folder = path.dirname(path.dirname(__file__))
"""Абсолютный путь к папке с игрой"""
graphics_folder = path.join(game_folder, 'assets/graphics')
"""Абсолютный путь к папке с графикой"""


def import_csv_layout(csv_path: str) -> list:
    """Позволяет читать csv файл из Tiled и преобразовывать в список
    -1 отсутствие тайла, 395, к примеру, стена
    """
    terrain_map = []
    with open(csv_path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(folder_path) -> list:
    """Загрузить в список все спрайты в папке"""
    surface_list = []

    for _, __, img_files in walk(folder_path):
        """folder_path = (path, [список папок внутри этой папки], [список img_files]), нам нужно только img_files"""
        for image in img_files:
            full_path = folder_path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_dict(folder_path) -> dict:
    """Загружает папку с изображениями в словарь"""
    surface_dict = {}

    for _, __, img_files in walk(folder_path):
        """folder_path = (path, [список папок внутри этой папки], [список img_files]), нам нужно только img_files"""
        for image in img_files:
            full_path = folder_path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf

    return surface_dict


def load_sprite(image_name: str):
    """Загружаем изображение"""
    try:
        image = pygame.image.load(f'{game_folder}/{image_name}')
    except FileNotFoundError as e:
        print('File not found, error: ', e)
        raise SystemExit()
    return image


if __name__ == '__main__':
    pass
