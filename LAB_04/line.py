"""Модуль для работы с прямыми.
"""
from typing import Tuple

import numpy as np

class Line():
    def __init__(self, x_points: np.ndarray, y_points: np.ndarray) -> None:
        self.k = None
        self.b = None
        self.x_points = x_points
        self.y_points = y_points

    def estimate_params(self) -> None:
        points_num = len(self.x_points)
        if points_num < 2:
            raise ValueError(f"Not enough points. Must be at least 2, but got {points_num}.")
        else:
            # подготовка данных для least-squares решения
            A = np.vstack([self.x_points, np.ones(len(self.x_points))]).T
            # вычисление
            self.k, self.b = np.linalg.lstsq(A, self.y_points, rcond=None)[0]

    # Получение данных k и b
    def get_params(self) -> Tuple[float, float]:
        return (self.k, self.b)

    # Задаём данные k и b
    def set_params(self, k: float, b: float) -> None:
        self.k = k
        self.b = b

    # [], с () в Tuple даёт ошибку
    def divide_points(self, x_points: np.ndarray, y_points: np.ndarray, eps: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        inliers_x = []
        inliers_y = []
        outliers_x = []
        outliers_y = []
        for kx, ky in zip(x_points, y_points):
            # сравниваем y и (kx - b), насколько близко
            if abs(ky - kx*self.k - self.b) < eps:
                inliers_x.append(kx)
                inliers_y.append(ky)
            else:
                outliers_x.append(kx)
                outliers_y.append(ky)
        return (inliers_x, inliers_y, outliers_x, outliers_y)