import sys
import numpy as np
import pygame as pg
from scipy.signal import convolve2d

# initiate pygame & load images
pg.init()
width, height = 1024, 640
Screen = pg.display.set_mode((width+260, height))
menu = pg.image.load('images\\gol_menu.png').convert()
Pause = pg.image.load('images\\gol_pause.png').convert()
slider = pg.image.load('images\\gol_slider.png').convert()
font = pg.font.SysFont('consolas', size=25)
clock = pg.time.Clock()

# initiate variables
pause, age, zoom, move_camera, zoom_coord = True, 0, 1, False, (int(width / 2), int(height / 2))
zoom_data, init_coord = [0, 0], 0
game_speeds, current_speed, move_slider, delay = {97: 5, 126: 10, 155: 30, 184: 45, 213: 60, 241: 500}, 241, False, 0
pre_pixels = np.zeros((width, height), dtype=int)
pixels = np.zeros((width, height), dtype=int)
zoom_pre_pixels = pre_pixels.copy()
zoom_pixels = pixels.copy()


def create(p, coor):
    """functions adds preset pattern to game, p is the name of pattern, coor is the coordinate to place pattern"""
    pattern = {'Queen_bee': np.array([[1, 0, 0, 0, 0],
                          [1, 0, 1, 0, 0],
                          [0, 1, 0, 1, 0],
                          [0, 1, 0, 0, 1],
                          [0, 1, 0, 1, 0],
                          [1, 0, 1, 0, 0],
                          [1, 0, 0, 0, 0]]),
               'R_pentomino': np.array([[0, 1, 1],
                                        [1, 1, 0],
                                        [0, 1, 0]]),
               'space_rake': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                                       [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                                       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                       [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                                       [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
               'p_24827M': np.array([[0, 0, 0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 1, 0, 1, 0, 0],
                         [1, 0, 0, 0, 0, 1, 0, 0],
                         [0, 1, 1, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 1, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 1, 1]]),
               'space_filler': np.array([[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                            [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]])}
    start_pattern = pattern.get(p, pattern['R_pentomino'])
    pixels[int(coor[0]):int(coor[0] + len(start_pattern)), int(coor[1]):int(coor[1] + len(start_pattern[0]))] = start_pattern


create('R_pentomino', [width/2, height/2])  # adds R pentomino to centre of grid

# I should have really used a class 
def zoom_draw():
    """functions draws live cells onto the grid, also rescales the grid when zooming in"""
    global zoom_pixels, zoom_pre_pixels, zoom_coord, zoom_data
    w1, h1 = int(width/zoom), int(height/zoom)
    xm, ym = zoom_coord = [min(max(zoom_coord[0], 0), width), min(max(zoom_coord[1], 0), height)]
    vec0, vec1 = int(xm-w1/2), int(ym-h1/2)
    corr0 = min(max(vec0, 0), width - w1)
    corr1 = min(max(vec1, 0), height - h1)
    zoom_pre_pixels = zoom_pixels.copy()
    zoom_pixels = pixels[corr0: corr0 + w1, corr1: corr1 + h1].copy()
    zoom_pixels = np.repeat(np.repeat(zoom_pixels, zoom, axis=0), zoom, axis=1)
    data = np.where(zoom_pre_pixels != zoom_pixels)
    for a, b in zip(data[0], data[1]):
        color = (255, 255, 255) if zoom_pixels[a, b] == 1 else (0, 0, 0)
        Screen.fill(color, ([a, b], (1, 1)))
    return w1, h1, corr0, corr1


def iteration(pixels):
    """updates cells every iteration using Conway's game of life rules.
       Divides the main grid into 16384 smaller grids, only updates grids with life in it"""

    def grid_split(w, h, coor0, coor1):
        """splits a grid into 4"""
        corners = [[0, w/2, 0, h/2], [w/2, w, 0, h/2], [0, w/2, h/2, h], [w/2, w, h/2, h]]
        for w1, w2, h1, h2 in corners:
            a1, a2, a3, a4 = int(w1 + coor0), int(w2 + coor0), int(h1 + coor1), int(h2 + coor1)
            box = pixels[a1:a2, a3:a4]
            box_extended = pixels[a1-2:a2+2, a3-2:a4+2]
            yield w1, h1, box_extended, box, np.sum(box)

    def game_rules(w, h, coor0, coor1):
        """updates grids"""
        sw, sh = int(width / 128), int(height / 128)
        for cx, cy, box_extended, box, empty in grid_split(w, h, coor0, coor1):
            if not empty:
                continue
            wi, hi = box.shape
            xl, yl = int(cx + coor0), int(cy + coor1)
            if wi == sw:
                kernal = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
                neighs = convolve2d(box_extended, kernal, mode='same')[1: sw + 3, 1:sh + 3]
                box_extended = box_extended[1: sw+3, 1:sh + 3]
                grid_selection = new_grid[-1 + xl:sw + 1 + xl, -1 + yl:sh + 1 + yl]
                grid_selection[(neighs == 3) | ((neighs == 2) & (box_extended == 1))] = 1
            else:
                game_rules(wi, hi, xl, yl)  # function is called recursively to split the grid into 4, seven times

    new_grid = np.zeros((width, height), dtype=int)
    game_rules(width, height, 0, 0)
    return new_grid


from numba import jit, b1
# faster code
@jit('b1[:, :](b1[:, :])', nopython=True)
def iteration_2(p):
    new_grid = np.zeros((width, height), dtype=b1)
    for i in range(1, width-1):
        for j in range(1, height-1):
            n = p[i-1][j+1] + p[i][j+1] + p[i+1][j+1] + p[i-1][j] + p[i+1][j] + p[i-1][j-1] + p[i][j-1] + p[i+1][j-1]
            new_grid[i][j] = (n == 3) | ((n == 2) & (p[i][j] == 1))
    return new_grid


def coordinate_change(mouse):
    """change coordinate of mouse depending on zoom"""
    zw1, zh1, corr0, corr1 = zoom_data
    xm = int((mouse[0] / width) * zw1 + corr0)
    ym = int((mouse[1] / height) * zh1 + corr1)
    return xm, ym


def print_text(text, coords):
    """print text to screen"""
    tool_text = font.render(text, True, (150, 150, 150))
    tool_text_rect = tool_text.get_rect(center=coords)
    Screen.blit(tool_text, tool_text_rect)


if __name__ == '__main__':
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            mx, my = pg.mouse.get_pos()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:     # reset
                    Screen.fill((0, 0, 0))
                    age = 0
                    pre_pixels = np.zeros((width, height), dtype=int)
                    pixels = np.zeros((width, height), dtype=int)
            if pg.mouse.get_pos()[0] <= width:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:   # animate/kill cell
                        index0, index1 = coordinate_change((mx, my))
                        pixels[index0, index1] ^= 1
                    elif event.button == 1:     # start panning
                        move_camera = True
                        init_coord = coordinate_change((mx, my))
                    elif event.button == 4:     # zoom in
                        zoom = min(int(zoom * 2), 32)
                        zoom_coord = coordinate_change((mx, my))
                    elif event.button == 5:     # zoom out
                        zoom = max(int(zoom / 2), 1)
                        zoom_coord = coordinate_change((mx, my))
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:   # stop panning
                        move_camera = False
            else:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if (width+9 <= mx <= width+85) and (173 <= my <= 249):  # pause/play
                        pause = not pause
                    if (width + current_speed <= mx <= width + current_speed + 10) and (176 <= my <= 197):  # fps slider
                        move_slider = True
                if event.type == pg.MOUSEBUTTONUP:
                    move_slider = False

        if move_camera:     # pan around the grid
            ix, iy = init_coord
            zx, zy = zoom_coord
            mx, my = coordinate_change(pg.mouse.get_pos())
            if (mx, my) != (ix, iy):
                zoom_coord = zx + ix - mx, zy + iy - my
        Screen.blit(menu, (width, 0))
        zoom_data = zoom_draw()     # draw pixels
        if not pause:   # iteration
            age += 1
            pre_pixels = pixels.copy()
            pixels = iteration(pixels)
        else:
            Screen.blit(Pause, (width+9, 173))
        if move_slider:     # fps slider
            mx, my = pg.mouse.get_pos()
            current_speed = min(list(game_speeds.keys()), key=lambda x: abs(x - mx + width))
        Screen.blit(slider, (width + current_speed, 176))

        print_text(str(round(clock.get_fps())), (width+146, 227))
        print_text(str(np.sum(pixels)), (width + 70, 298))
        print_text(str(age), (width + 188, 298))

        zw, zh, c0, c1 = zoom_data
        corner_rect = [int(width + 2 + c0/4), int(2 + c1/4), int(zw/4), int(zh/4)]
        pg.draw.rect(Screen, (0, 200, 0), corner_rect, 1)

        pg.display.update()
        clock.tick(game_speeds[current_speed])
