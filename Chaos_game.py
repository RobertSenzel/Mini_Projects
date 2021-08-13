import sys
import numpy as np
import pygame as pg


def sierpinski_gasket():
    pg.init()
    w, h = 1300, 600
    Screen = pg.display.set_mode((w, h))
    pg.display.set_caption('Sierpinski Gasket')
    points = []
    triangle = [np.array([int(w/2), 10]), np.array([int(w/4), h-10]), np.array([int(0.75*w), h-10])]

    pg.draw.polygon(Screen, (255, 255, 255), triangle, 1)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if (event.type == pg.MOUSEBUTTONDOWN) and (event.button == 1):
                points.append(np.array(pg.mouse.get_pos()))

        if len(points) >= 1:
            Screen.fill((255, 255, 255), (points[-1].astype(int), (1, 1)))
            random_corner = triangle[np.random.choice([0, 1, 2])]
            points.append((random_corner+points[-1])/2)

        pg.display.update()
        
        
def Barnsley_fern():
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

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        Screen.fill((0, 200, 0), (coordinate_change(points[-1]), (1, 1)))
        points.append(transform(points[-1], np.random.choice([0, 1, 2, 3], p=[0.01, 0.85, 0.07, 0.07])))
        pg.display.update()
        
        
if __name__ == '__main__':
    sierpinski_gasket()
