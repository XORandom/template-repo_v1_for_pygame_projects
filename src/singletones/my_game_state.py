
# /// script
# requires-python = ">=3.12"
# dependencies = []
# [tool.uv]
# exclude-newer = "2025-02-12T00:00:00Z"
# ///



"""
Функции, определяющие текущее состояние игры, упрощают переключение сцен.
"""


class GameState:
    def __init__(self, initial_state):
        self.state = initial_state
        """Текущее состояние игры"""
        self.previous_state = None
        """Предыдущее состояние игры"""

    def get_state(self):
        """Узнать текущую сцену"""
        return self.state

    def set_state(self, new_state):
        """Установить текущую сцену"""
        self.previous_state = self.state
        self.state = new_state

    def get_previous_state(self):
        """Узнать, какая сцена была у игры до этого"""
        print(self.previous_state)
        return self.previous_state

if __name__ == '__main__':
    pass














