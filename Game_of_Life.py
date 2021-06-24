import sys
# import time
import numpy as np
import pygame as pg
import gol_patterns as gp
from scipy.signal import convolve2d

pg.init()
width, height = 1024, 640
Screen = pg.display.set_mode((width+260, height))
menu = pg.image.load('pics_random\\game_of_life.png').convert()
Pause = pg.image.load('pics_random\\pause.png').convert()
slider = pg.image.load('pics_random\\slider.png').convert()
font = pg.font.SysFont('consolas', size=25)
clock = pg.time.Clock()


pg.display.set_caption('Game of life')
pause, zoom, zoom_limit, zoom_follow, zoom_coord = True, 1, 32, False, (int(width/2), int(height/2))
zoom_data, init_zoom = [0, 0], 0
speeds, slider_loc, slider_follow = {97: 5, 126: 10, 155: 30, 184: 45, 213: 60, 241: 500}, 241, False
draw_data, draw_pattern = [0, 0], False
kernal = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
pre_step = np.zeros((width, height), dtype=int)
pixels = np.zeros((width, height), dtype=int)
zoom_pre_step = pre_step.copy()
zoom_pixels = pixels.copy()


def create(pattern, corr):
    pixels[int(corr[0]):int(corr[0]+len(pattern)), int(corr[1]):int(corr[1]+len(pattern[0]))] = pattern


create(gp.spacefiller, [width/2, height/2])


def zoom_draw():
    global zoom_pixels, zoom_pre_step, zoom_coord, zoom_data
    w1, h1 = int(width/zoom), int(height/zoom)
    zoom_coord = [min(max(zoom_coord[0], 0), width), min(max(zoom_coord[1], 0), height)]
    xm, ym = zoom_coord
    vec0, vec1 = int(xm-w1/2), int(ym-h1/2)
    corr0 = min(max(vec0, 0), width - w1)
    corr1 = min(max(vec1, 0), height - h1)
    zoom_pre_step = zoom_pixels.copy()
    zoom_pixels = pixels[corr0: corr0 + w1, corr1: corr1 + h1].copy()
    zoom_pixels = np.repeat(np.repeat(zoom_pixels, zoom, axis=0), zoom, axis=1)
    data = np.where(zoom_pre_step != zoom_pixels)
    for a, b in zip(data[0], data[1]):
        color = (255, 255, 255) if zoom_pixels[a, b] == 1 else (0, 0, 0)
        Screen.fill(color, ([a, b], (1, 1)))
    return w1, h1, corr0, corr1


def iteration():
    global pixels

    def cut(w, h, corr0, corr1):
        corners = [[0, w/2, 0, h/2], [w/2, w, 0, h/2], [0, w/2, h/2, h], [w/2, w, h/2, h]]
        for w1, w2, h1, h2 in corners:
            a1, a2, a3, a4 = int(w1 + corr0), int(w2 + corr0), int(h1 + corr1), int(h2 + corr1)
            box = pixels[a1:a2, a3:a4]
            box_extended = pixels[a1-2:a2+2, a3-2:a4+2]
            yield w1, h1, box_extended, box, np.sum(box)

    def grid_recursion(w, h, corr0, corr1):
        sw, sh = int(width / 128), int(height / 128)
        for cx, cy, box_extended, box, empty in cut(w, h, corr0, corr1):
            if not empty:
                continue
            wi, hi = box.shape
            xl, yl = int(cx + corr0), int(cy + corr1)
            if wi == sw:
                neighs = convolve2d(box_extended, kernal, mode='same')[1: sw+3, 1:sh + 3]
                box_extended = box_extended[1: sw+3, 1:sh + 3]
                grid_selection = new_grid[-1 + xl:sw + 1 + xl, -1 + yl:sh + 1 + yl]
                grid_selection[(neighs == 3) | ((neighs == 2) & (box_extended == 1))] = 1
            else:
                grid_recursion(wi, hi, xl, yl)

    new_grid = np.zeros((width, height), dtype=int)
    grid_recursion(width, height, 0, 0)
    return new_grid


def mouse_coord(mouse):
    zw1, zh1, corr0, corr1 = zoom_data
    xm = int((mouse[0] / width) * zw1 + corr0)
    ym = int((mouse[1] / height) * zh1 + corr1)
    return xm, ym


if __name__ == '__main__':
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            mx, my = pg.mouse.get_pos()
            if pg.mouse.get_pos()[0] <= width:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        index0, index1 = mouse_coord((mx, my))
                        pixels[index0, index1] ^= 1
                    elif event.button == 2:
                        draw_pattern = True
                    elif event.button == 1:
                        zoom_follow = True
                        init_zoom = mouse_coord((mx, my))
                    elif event.button == 4:
                        zoom = min(int(zoom * 2), zoom_limit)
                        zoom_coord = mouse_coord((mx, my))
                    elif event.button == 5:
                        zoom = max(int(zoom / 2), 1)
                        zoom_coord = mouse_coord((mx, my))
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        zoom_follow = False
                        init_zoom = 0
                    if event.button == 2:
                        draw_pattern = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_d:
                        draw_pattern = True
                        wd = int(input('width: '))
                        hd = int(input('height: '))
                        draw_data = wd, hd
                        pixels[int(width/2-1):int(width/2+1)+wd, int(height/2-1)] = 1
                        pixels[int(width / 2 - 1):int(width / 2 + 1) + wd, int(height / 2) + hd] = 1
                        pixels[int(width / 2 - 1), int(height / 2 - 1): int(height / 2 + 1) + hd] = 1
                        pixels[int(width / 2)+wd, int(height / 2 - 1): int(height / 2 + 1) + hd] = 1
                    if event.key == pg.K_f:
                        draw_pattern = False
                        a1, a2 = draw_data
                        pattern_save = pixels[int(width/2):int(width/2)+a1, int(height/2):int(height/2)+a2]
                        np.save('space',  pattern_save)
                    if event.key == pg.K_r:
                        Screen.fill((0, 0, 0))
                        pre_step = np.zeros((width, height), dtype=int)
                        pixels = np.zeros((width, height), dtype=int)
                        zoom_pre_step = pre_step.copy()
                        zoom_pixels = pixels.copy()
            else:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if (width+9 <= mx <= width+85) and (173 <= my <= 249):
                        pause = not pause
                    if (width+slider_loc <= mx <= width+slider_loc+10) and (176 <= my <= 197):
                        slider_follow = True
                if event.type == pg.MOUSEBUTTONUP:
                    slider_follow = False

        if zoom_follow:
            ix, iy = init_zoom
            zx, zy = zoom_coord
            mx, my = mouse_coord(pg.mouse.get_pos())
            if (mx, my) != (ix, iy):
                zoom_coord = zx + ix - mx, zy + iy - my
        if draw_pattern:
            index0, index1 = mouse_coord(pg.mouse.get_pos())
            pixels[index0, index1] = 1
        Screen.blit(menu, (width, 0))
        zoom_data = zoom_draw()
        if not pause:
            pre_step = pixels.copy()
            pixels = iteration()
        else:
            Screen.blit(Pause, (width+9, 173))
        if slider_follow:
            mx, my = pg.mouse.get_pos()
            slider_loc = min(list(speeds.keys()), key=lambda x: abs(x-mx+width))
        Screen.blit(slider, (width + slider_loc, 176))
        tool_text = font.render(str(round(clock.get_fps())), True, (150, 150, 150))
        tool_text_rect = tool_text.get_rect(center=(width+146, 227))
        Screen.blit(tool_text, tool_text_rect)

        zw, zh, c0, c1 = zoom_data
        corner_rect = [int(width + 2 + c0/4), int(2 + c1/4), int(zw/4), int(zh/4)]
        pg.draw.rect(Screen, (0, 200, 0), corner_rect, 1)

        pg.display.update()
        clock.tick(speeds[slider_loc])
