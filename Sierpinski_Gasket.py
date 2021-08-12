import sys
import numpy as np
import pygame as pg

pg.init()
w, h = 1300, 600
Screen = pg.display.set_mode((w, h))
pg.display.set_caption('Sierpinski Gasket')
points = []
triangle = [np.array([int(w/2), 10]), np.array([int(w/4), h-10]), np.array([int(0.75*w), h-10])]

if __name__ == '__main__':
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
