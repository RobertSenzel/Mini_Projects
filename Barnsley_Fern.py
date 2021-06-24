import sys
import numpy as np
import pygame as pg

pg.init()
Screen = pg.display.set_mode((900, 600))
pg.display.set_caption('Barnsley Fern')
points = [np.array([0, 0])]


def transform(point, n):
    matrices = [np.array([[0, 0], [0, 0.16]]), np.array([[0.85, 0.04], [-0.04, 0.85]]),
                np.array([[0.2, -0.26], [0.23, 0.22]]), np.array([[-0.15, 0.28], [0.26, 0.24]])]
    addons = [np.array([0, 0]), np.array([0, 1.6]), np.array([0, 1.6]), np.array([0, 0.44])]
    return np.dot(matrices[n], point) + addons[n]


def coordinate_change(point):
    matrix = np.array([[1, 0, 9], [0, -1, 11], [0, 0, 1]])
    point = np.dot(matrix, np.append(point, 1)*50)
    return point[:2].astype(int)


if __name__ == '__main__':
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        Screen.fill((0, 200, 0), (coordinate_change(points[-1]), (1, 1)))
        points.append(transform(points[-1], np.random.choice([0, 1, 2, 3], p=[0.01, 0.85, 0.07, 0.07])))
        pg.display.update()
