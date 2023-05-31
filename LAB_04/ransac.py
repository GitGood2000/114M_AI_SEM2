"""
RANSAC for 2d lines
Algorythm:

I Hypotesys generation Stage
1. Sample 2d points (1. 2 ponts; 2. 5 points)
2. Model estimation (1. analytics; 2. MSE estimation)

II Hypotesys evaluation Stage

3. Inlier counting (%inlinear > threshold) 
    if True -> best params
    if False -> 1.
4. # iter > num_iter?

"""

import numpy as np

import matplotlib.pyplot as plt

from line import Line

class RANSAC:
    def __init__(self) -> None:
        self.iter_num: int = 100
        self.line_points: int = 2 # счётчик точек, по которым строим линию
        self.inlin_thrsh: float = 0.8
        self.epsilon: float = 0.1
        self.best_params: dict = {}
        self.inlinears_x: list = [] # почти касаются линии
        self.inlinears_y: list = []
        self.outliers_x: list = [] # далеки от линии
        self.outliers_y: list = []
        self.score: int = 0
        self.x_points: np.ndarray = None
        self.y_points: np.ndarray = None

    # Задаём данные
    def set_case(self, case_params) -> None:
        # проверка наличия ключа iter_num
        if 'iter_num' in case_params.keys():
            # задаём ключ в case_params
            self.iter_num = case_params['iter_num']
        # аналогично для остального
        if 'line_points' in case_params.keys():
            self.n_pointsy = case_params['line_points']
        if 'inlin_thrsh' in case_params.keys():
            self.inlin_thrsh = case_params['inlin_thrsh']
        if 'epsilon' in case_params.keys():
            self.epsilon = case_params['epsilon']
        if not ('x' in case_params.keys() and 'y' in case_params.keys()):
            raise ValueError(f"case_params обязан включать в себя ключи 'x' и 'y'")
        self.x_points = case_params['x']
        self.y_points = case_params['y']

    # очищаем данные
    def clear_case(self) -> None:
        self.__init__()

    def fit(self):
        for i in range(self.iter_num):
            ind = range(len(self.x_points)) #массив от 0 до кол-ва данных
            ind_samples = np.random.choice(ind, self.line_points) #кол-во данных для построения
            # разделяем на x и y для упрощения использования numpy-функций
            x_samples = self.x_points[ind_samples]
            y_samples = self.y_points[ind_samples]
            line = Line(x_samples, y_samples)
            line.estimate_params()
            # разбиваем на in и out (по x и y)
            inlnrs_x, inlnrs_y, outlnrs_x, outlnrs_y = line.divide_points(self.x_points, self.y_points, self.epsilon)
            score = len(inlnrs_x) / len(self.x_points) # accuracy
            if score > self.score:
                k, b = line.get_params()
                self.best_params = [k, b]
                self.score = score
                self.inlinears_x = inlnrs_x
                self.inlinears_y = inlnrs_y
                self.outliers_x = outlnrs_x
                self.outliers_y = outlnrs_y


    def draw(self):
        plt.plot(self.inlinears_x, self.inlinears_y, 'x', label='inlinears')
        plt.plot(self.outliers_x, self.outliers_y, 'x', label='outliers')
        plt.plot(self.x_points, self.best_params[0]*self.x_points + self.best_params[1], 'r', label='Fitted line')
        plt.legend()
        plt.show()