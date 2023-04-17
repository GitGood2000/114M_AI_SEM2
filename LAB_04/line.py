"""Модуль для работы с прямыми.
"""
from typing import Tuple

import numpy as np

class Line():
    def __init__(self, points: np.ndarray) -> None:
        self.k = None
        self.b = None
        self.points = points

    def estimate_params(self) -> None:
        points_num = len(self.points)
        if points_num > 2:
            raise NotImplementedError
        elif points_num < 2:
            raise ValueError(f"Not enough points. Must be at least 2, but got {points_num}.")
        else:
            x1, y1 = self.points[0]
            x2, y2 = self.points[1]
            self.k =
            self.b =

    def devide_points(self, points: np.ndarray, eps: float) -> Tuple(np.ndarray, np.ndarray):
        pass
