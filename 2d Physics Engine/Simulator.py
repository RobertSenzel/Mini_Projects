import sys
import numpy as np
import pygame as pg
from itertools import combinations

import Circle_code as Cc
import Rectangle_code as Rc

pg.init()
Screen = pg.display.set_mode((1260, 640))
pg.display.set_caption('Physics_Engine')
clock = pg.time.Clock()

border = pg.image.load('Menu_Images\\border.png').convert_alpha()
play = pg.image.load('Menu_Images\\Play.png').convert_alpha()
pause = pg.image.load('Menu_Images\\Pause.png').convert_alpha()

field_menu = pg.image.load('Menu_Images\\Field_Menu.png').convert_alpha()
field_pointer = pg.image.load('Menu_Images\\Field_Pointer.png').convert_alpha()
field_slider = pg.image.load('Menu_Images\\Field_Slider.png').convert_alpha()

object_menu = pg.image.load('Menu_Images\\Object_Menu.png').convert_alpha()

Menu_state = object_menu
Sim_state = pause

selected_object = []
circle_objects = []
rect_objects = []
velocity_mover = False
size_mover = False


class UserFieldTools:
    def __init__(self, coordinates, tool_data, image, text, tool_type, active=False, start=0):
        self.coordinates = coordinates
        self.active = active
        self.tool_data = tool_data
        self.image = image
        self.text_coordinates = text[0]
        self.tool_type = tool_type
        self.start = start
        self.font = pg.font.SysFont('consolas', size=text[1])
        self.rect = self.image.get_rect(center=coordinates)

    def draw(self, screen):
        tool_text = self.font.render(str(round(self.tool_data)), True, (0, 0, 0))
        tool_text_rect = tool_text.get_rect(center=self.text_coordinates)
        screen.blit(tool_text, tool_text_rect)
        rot = pg.transform.rotate(self.image, self.tool_data) if self.tool_type == 'rotate_pointer' else self.image
        draw_rot_rect = rot.get_rect(center=self.coordinates)
        screen.blit(rot, draw_rot_rect)

    def mouse_check(self):
        return self.rect.collidepoint(pg.mouse.get_pos())

    def mouse_update(self):
        if self.active:
            x, y = pg.mouse.get_pos()
            if self.tool_type == 'horizontal_slider':
                if self.start <= x <= self.start + 100:
                    self.coordinates[0] = x
                elif x < self.start:
                    self.coordinates[0] = self.start
                else:
                    self.coordinates[0] = self.start + 100
                self.tool_data = self.coordinates[0] - self.start
            elif self.tool_type == 'vertical_slider':
                if self.start >= y >= self.start - 100:
                    self.coordinates[1] = y
                elif y > self.start:
                    self.coordinates[1] = self.start
                else:
                    self.coordinates[1] = self.start - 100
                self.tool_data = self.start - self.coordinates[1]
            elif self.tool_type == 'rotate_pointer':
                sign = 1 if pg.mouse.get_pos()[0] <= 70 else -1
                vector = np.array([x, y]) - np.array(self.coordinates)
                norm = np.linalg.norm(vector)
                self.tool_data = sign * np.rad2deg(np.arccos(np.dot(vector / norm, np.array([0, -1]))))
            self.rect = self.image.get_rect(center=self.coordinates)


class UserObjectTools:
    def __init__(self, coordinates, tool_data, tool_type, font_size, active=False):
        self.active = active
        self.tool_data = tool_data
        self.tool_type = tool_type
        self.font = pg.font.SysFont('consolas', size=font_size) if font_size != 0 else 0
        self.rect = pg.Rect(coordinates)

    def draw(self, screen):
        if self.tool_type == 'object_text':
            if selected_object:
                if self.tool_data == 'center':
                    if selected_object[0].shape() == 'circle':
                        cent = selected_object[0].center
                    elif selected_object[0].shape() == 'rect':
                        cent = selected_object[0].center()
                    else:
                        cent = ['','']
                    text = f"{round(cent[0])},{round(cent[1])}"
                elif self.tool_data == 'speed':
                    text = f"{round(np.linalg.norm(selected_object[0].velocity), 1)}"
                elif self.tool_data == 'density':
                    text = f"{selected_object[0].density}"
                elif self.tool_data == 'mass':
                    text = f"{round(selected_object[0].mass())}"
                elif self.tool_data == 'charge':
                    text, sign = f"{abs(selected_object[0].charge)}", np.sign(selected_object[0].charge)
                    if sign != -1:
                        pg.draw.rect(screen, (156, 156, 156), pg.Rect([94, 282, 3, 13]))
                elif self.tool_data == 'rotate':
                    text, sign = f"{abs(round(selected_object[0].rotate,2))}", np.sign(selected_object[0].rotate)
                    if sign != -1:
                        pg.draw.rect(screen, (156, 156, 156), pg.Rect([94, 304, 3, 13]))
                elif self.tool_data == 'colour':
                    col = selected_object[0].colour
                    text = f"{'{:0>3d}'.format(col[0])},{'{:0>3d}'.format(col[1])},{'{:0>3d}'.format(col[2])}"
                elif self.tool_data == 'length':
                    if selected_object[0].shape() == 'circle':
                        text = f"{2 * selected_object[0].radius}"
                    elif selected_object[0].shape() == 'rect':
                        text = f"{round(selected_object[0].size()[0])}"
                    else:
                        text = 'N/A'
                elif self.tool_data == 'width':
                    if selected_object[0].shape() == 'circle':
                        text = f"{2 * selected_object[0].radius}"
                    elif selected_object[0].shape() == 'rect':
                        text = f"{round(selected_object[0].size()[1])}"
                    else:
                        text = 'N/A'
                elif self.tool_data == 'area':
                    if selected_object[0].shape() == 'circle':
                        text = f"{round(np.pi * selected_object[0].radius**2)}"
                    elif selected_object[0].shape() == 'rect':
                        text = f"{round(selected_object[0].area())}"
                    else:
                        text = 'N/A'
                else:
                    text = f"{round(clock.get_fps())}"
                tool_text = self.font.render(text, True, (156, 156, 156))
                screen.blit(tool_text, self.rect)
        elif self.tool_type == 'abilities':
            if selected_object:
                coord_abl = {'no_move': [1, [107, 512, 10, 10]], 'ghost': [0, [107, 528, 10, 10]],
                             'rotate': [0, [107, 544, 10, 10]], 'portal': [0, [107, 560, 10, 10]],
                             'follow': [0, [107, 576, 10, 10]]}
                data = coord_abl[self.tool_data]
                if self.tool_data in selected_object[0].properties:
                    pg.draw.rect(screen, (0, 156, 0), data[1]) if data[0] == 0 else None
                else:
                    pg.draw.rect(screen, (0, 156, 0), data[1]) if data[0] == 1 else None
        elif self.tool_type == 'mover' or self.tool_type == 'size_mover':
            if self.active:
                pg.draw.rect(screen, (0, 156, 0), self.rect, 1)
        elif self.tool_type == 'vel_mover':
            if self.active:
                pg.draw.rect(screen, (0, 156, 0), self.rect, 1)
                if self.tool_data and np.linalg.norm(self.tool_data[0].velocity) != 0:
                    cent_obj = self.tool_data[0].center if selected_object[0].shape() == 'circle' else \
                        self.tool_data[0].center()
                    cent = np.round(cent_obj).astype(int)
                    velo = self.tool_data[0].velocity
                    norm = np.linalg.norm(velo)
                    rad = self.tool_data[0].radius if selected_object[0].shape() == 'circle' else \
                        self.tool_data[0].size()[0]
                    endpoint = np.round(cent_obj + (velo*(50+rad))/norm).astype(int)
                    pg.draw.line(screen, (0, 0, 0), cent, endpoint, 2)
        else:
            pass

    def mouse_check(self):
        if self.tool_type == 'mover' or self.tool_type == 'vel_mover' or self.tool_type == 'size_mover':
            x, y = pg.mouse.get_pos()
            return self.rect.collidepoint(x, y)
        else:
            return False

    def mouse_update(self, vel_move, size_move):
        x, y = pg.mouse.get_pos()
        if self.active and (self.tool_data != []) and (x > 201):
            if selected_object[0].shape() == 'circle':
                if self.tool_type == 'mover':
                    self.tool_data[0].center = np.array([x, y]).astype(float)
                elif (self.tool_type == 'vel_mover') and vel_move:
                    speed = np.linalg.norm(self.tool_data[0].velocity)
                    new_vel = np.array([x, y]) - self.tool_data[0].center
                    norm = np.linalg.norm(new_vel)
                    self.tool_data[0].velocity = (new_vel*speed)/norm
                elif (self.tool_type == 'size_mover') and size_move:
                    self.tool_data[0].radius = (np.linalg.norm(np.array([x, y]) - self.tool_data[0].center)).astype(int)
            elif selected_object[0].shape() == 'rect':
                if self.tool_type == 'mover':
                    h, k = np.array([x, y]).astype(float) - self.tool_data[0].center()
                    matrix = np.array([[1, 0, h], [0, 1, k], [0, 0, 1]])
                    self.tool_data[0].corners = np.dot(matrix, self.tool_data[0].corners.T).T
                elif (self.tool_type == 'vel_mover') and vel_move:
                    speed = np.linalg.norm(self.tool_data[0].velocity)
                    new_vel = np.array([x, y]) - self.tool_data[0].center()
                    norm = np.linalg.norm(new_vel)
                    self.tool_data[0].velocity = (new_vel * speed) / norm
                elif (self.tool_type == 'size_mover') and size_move:
                    mouse_vec = np.array([x, y, 1])
                    corners = self.tool_data[0].corners
                    minp = min(corners, key=(lambda cor: np.linalg.norm(mouse_vec-cor)))
                    maxp = max(corners, key=(lambda cor: np.linalg.norm(mouse_vec-cor)))
                    opps = [i for i in corners if list(i) not in [list(minp), list(maxp)]]
                    opps_vec1, opps_vec2 = opps[0] - maxp, opps[1] - maxp
                    point = mouse_vec - maxp
                    proj1 = (np.dot(opps_vec1, point) / np.linalg.norm(opps_vec1) ** 2) * opps_vec1
                    proj2 = (np.dot(opps_vec2, point) / np.linalg.norm(opps_vec2) ** 2) * opps_vec2
                    self.tool_data[0].corners = np.array([maxp, maxp + proj1, mouse_vec, maxp + proj2])


def ObjectStatUpdater(obj):
    global circle_objects, rect_objects, selected_object
    mx, my = pg.mouse.get_pos()
    if (172 <= mx <= 188) and (94 <= my <= 110):
        circle_objects.clear()
        rect_objects.clear()
        selected_object.clear()
    if obj:
        if (164 <= mx <= 174) and my < 400:
            if 213 <= my <= 221:
                speed = np.linalg.norm(obj[0].velocity)
                obj[0].velocity = (obj[0].velocity / speed) * (speed + 1) if speed != 0.0 else np.array([0.0, -1.0])
            elif 223 <= my <= 231:
                speed = np.linalg.norm(obj[0].velocity)
                limit = 1 if speed < 1 else speed
                obj[0].velocity = (obj[0].velocity / speed) * (limit - 1) if speed != 0.0 else np.array([0.0, 0.0])
            elif 235 <= my <= 243:
                obj[0].density += 10
            elif 245 <= my <= 253:
                obj[0].density -= 10
            elif 279 <= my <= 287:
                obj[0].charge += 1
            elif 289 <= my <= 297:
                obj[0].charge -= 1
            elif 301 <= my <= 309:
                obj[0].rotate += 0.01
            elif 311 <= my <= 319:
                obj[0].rotate -= 0.01
                if abs(obj[0].rotate) < 0.01:
                    obj[0].rotate = 0.0
        elif (101 <= mx <= 111) and (344 <= my <= 352):
            obj[0].colour[0] += 51
            obj[0].colour[0] = 255 if obj[0].colour[0] > 255 else obj[0].colour[0]
        elif (101 <= mx <= 111) and (354 <= my <= 362):
            obj[0].colour[0] -= 51
            obj[0].colour[0] = 0 if obj[0].colour[0] < 0 else obj[0].colour[0]
        elif (126 <= mx <= 136) and (344 <= my <= 352):
            obj[0].colour[1] += 51
            obj[0].colour[1] = 255 if obj[0].colour[1] > 255 else obj[0].colour[1]
        elif (126 <= mx <= 136) and (354 <= my <= 362):
            obj[0].colour[1] -= 51
            obj[0].colour[1] = 0 if obj[0].colour[1] < 0 else obj[0].colour[1]
        elif (150 <= mx <= 160) and (344 <= my <= 352):
            obj[0].colour[2] += 51
            obj[0].colour[2] = 255 if obj[0].colour[2] > 255 else obj[0].colour[2]
        elif (150 <= mx <= 160) and (354 <= my <= 362):
            obj[0].colour[2] -= 51
            obj[0].colour[2] = 0 if obj[0].colour[2] < 0 else obj[0].colour[2]
        elif 160 <= mx <= 170:
            if obj[0].shape() == 'circle':
                if (404 <= my <= 412) or (426 <= my <= 434):
                    obj[0].radius += 1
                elif (414 <= my <= 422) or (436 <= my <= 444):
                    obj[0].radius -= 1
            elif obj[0].shape() == 'rect':
                vec1, vec2 = obj[0].corners[3] - obj[0].corners[0],  obj[0].corners[1] - obj[0].corners[0]
                len1, len2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
                corr1, corr2 = vec1 * (len1 + 1) / len1, vec2 * (len2 + 1) / len2
                corr1m, corr2m = vec1 * (len1 - 1) / len1, vec2 * (len2 - 1) / len2
                if 404 <= my <= 412:
                    if len1 >= len2:
                        obj[0].corners[3] = obj[0].corners[0] + corr1
                        obj[0].corners[2] = obj[0].corners[0] + corr1 + vec2
                    else:
                        obj[0].corners[1] = obj[0].corners[0] + corr2
                        obj[0].corners[2] = obj[0].corners[0] + corr2 + vec1
                elif 414 <= my <= 422:
                    if len1 >= len2:
                        obj[0].corners[3] = obj[0].corners[0] + corr1m
                        obj[0].corners[2] = obj[0].corners[0] + corr1m + vec2
                    else:
                        obj[0].corners[1] = obj[0].corners[0] + corr2m
                        obj[0].corners[2] = obj[0].corners[0] + corr2m + vec1
                elif 426 <= my <= 434:
                    if len1 >= len2:
                        obj[0].corners[1] = obj[0].corners[0] + corr2
                        obj[0].corners[2] = obj[0].corners[0] + corr2 + vec1
                    else:
                        obj[0].corners[3] = obj[0].corners[0] + corr1
                        obj[0].corners[2] = obj[0].corners[0] + corr1 + vec2
                elif 436 <= my <= 444:
                    if len1 >= len2:
                        obj[0].corners[1] = obj[0].corners[0] + corr2m
                        obj[0].corners[2] = obj[0].corners[0] + corr2m + vec1
                    else:
                        obj[0].corners[3] = obj[0].corners[0] + corr1m
                        obj[0].corners[2] = obj[0].corners[0] + corr1m + vec2

        elif (147 <= mx <= 163) and (94 <= my <= 110):
            if obj[0].shape() == 'circle':
                circle_objects.remove(selected_object[0])
            elif obj[0].shape() == 'rect':
                rect_objects.remove(selected_object[0])
            selected_object.clear()
        elif (88 <= mx <= 102) and (281 <= my <= 295):
            obj[0].charge *= -1
        elif (88 <= mx <= 102) and (303 <= my <= 317):
            obj[0].rotate *= -1
        elif 107 <= mx <= 116:
            if 512 <= my <= 521:
                if 'no_move' in selected_object[0].properties:
                    selected_object[0].properties.remove('no_move')
                else:
                    selected_object[0].properties.append('no_move')
            elif 528 <= my <= 537:
                if 'ghost' in selected_object[0].properties:
                    selected_object[0].properties.remove('ghost')
                else:
                    selected_object[0].properties.append('ghost')
            elif 544 <= my <= 553:
                if 'rotate' in selected_object[0].properties:
                    selected_object[0].properties.remove('rotate')
                else:
                    selected_object[0].properties.append('rotate')


def user_tool_collection():
    field_menu_tools = [UserFieldTools([70, 171], 180, field_pointer, [[114, 123], 11], 'rotate_pointer'),
                        UserFieldTools([70, 317], 0, field_pointer, [[114, 269], 11], 'rotate_pointer'),
                        UserFieldTools([148, 221], 0, field_slider, [[169, 100], 16], 'vertical_slider', start=221),
                        UserFieldTools([148, 367], 0, field_slider, [[169, 245], 16], 'vertical_slider', start=367),
                        UserFieldTools([29, 396], 0, pg.transform.rotate(field_slider, 90), [[163, 397], 16],
                                       'horizontal_slider', start=29),
                        UserFieldTools([29, 424], 0, pg.transform.rotate(field_slider, 90), [[163, 425], 16],
                                       'horizontal_slider', start=29),
                        UserFieldTools([37, 621], 0, field_slider, [[37, 499], 16], 'vertical_slider', start=621),
                        UserFieldTools([114, 621], 0, field_slider, [[114, 499], 16], 'vertical_slider', start=621),
                        UserFieldTools([162, 621], 0, field_slider, [[0, 0], 0], 'vertical_slider', start=621)]

    object_menu_tools = [UserObjectTools([178, 192, 17, 17], [], 'mover', 0),
                         UserObjectTools([178, 214, 17, 17], [], 'vel_mover', 0),
                         UserObjectTools([57, 374, 19, 19], [], 'size_mover', 0),
                         UserObjectTools([100, 194, 54, 17], 'center', 'object_text', 13),
                         UserObjectTools([110, 216, 54, 17], 'speed', 'object_text', 13),
                         UserObjectTools([110, 238, 54, 17], 'density', 'object_text', 13),
                         UserObjectTools([106, 260, 54, 17], 'mass', 'object_text', 13),
                         UserObjectTools([130, 282, 54, 17], 'charge', 'object_text', 13),
                         UserObjectTools([113, 304, 54, 17], 'rotate', 'object_text', 13),
                         UserObjectTools([92, 326, 54, 17], 'colour', 'object_text', 13),
                         UserObjectTools([120, 407, 54, 17], 'length', 'object_text', 13),
                         UserObjectTools([120, 429, 54, 17], 'width', 'object_text', 13),
                         UserObjectTools([115, 451, 54, 17], 'area', 'object_text', 13),
                         UserObjectTools([107, 512, 10, 10], 'no_move', 'abilities', 13),
                         UserObjectTools([107, 528, 10, 10], 'ghost', 'abilities', 13),
                         UserObjectTools([107, 544, 10, 10], 'rotate', 'abilities', 13),
                         UserObjectTools([107, 560, 10, 10], 'portal', 'abilities', 13),
                         UserObjectTools([107, 576, 10, 10], 'follow', 'abilities', 13),
                         UserObjectTools([59, 96, 53, 15], 'fps', 'object_text', 14)]

    return field_menu_tools, object_menu_tools


field_tools, object_tools = user_tool_collection()


def area_triangle(a, b, c):
    return abs(a[0]*(b[1] - c[1]) + b[0]*(c[1] - a[1]) + c[0]*(a[1] - b[1])) / 2


def object_selector(prev_select, pos):
    x, y = pos
    if (x < 201) or object_tools[1].active or object_tools[2].active:
        return prev_select
    for circle in circle_objects:
        if np.linalg.norm(circle.center-np.array([x, y])) <= circle.radius:
            return [circle]
    for rect in rect_objects:
        axy, bxy, cxy, dxy = rect.corners
        area1 = area_triangle(axy, bxy, pos)
        area2 = area_triangle(bxy, cxy, pos)
        area3 = area_triangle(cxy, dxy, pos)
        area4 = area_triangle(dxy, axy, pos)
        if (area1 + area2 + area3 + area4) <= rect.area():
            return [rect]
    return []


def user_input():
    global Sim_state, Menu_state, selected_object, velocity_mover, size_mover

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        mx, my = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (11 <= mx <= 75) and (12 <= my <= 76):
                    Sim_state = play if Sim_state == pause else pause
                elif (105 <= mx <= 124) and (12 <= my <= 31):
                    Menu_state = field_menu
                elif (83 <= mx <= 102) and (12 <= my <= 31):
                    Menu_state = object_menu
                elif Menu_state == field_menu:
                    for tool in field_tools:
                        if tool.mouse_check():
                            tool.active = True
                elif Menu_state == object_menu:
                    if (11 <= mx <= 53) and (118 <= my <= 161):
                        new_circle = Cc.Circle([mx, my], [0, 0], [0, 102, 153], 17, 50, 1, 0, ['no_move'])
                        circle_objects.append(new_circle)
                        object_tools[0].active = True
                        object_tools[1].active = False
                        object_tools[2].active = False
                        object_tools[0].tool_data = selected_object = [new_circle]
                    elif (56 <= mx <= 98) and (118 <= my <= 161):
                        corners = [[63, 128, 1], [91, 128, 1], [91, 150, 1], [63, 150, 1]]
                        props = ['no_move', 'rotate']
                        new_rect = Rc.Rectangle(corners, [0, 0], [200, 0, 0], 50, 1, props, e=1, rotate=0)
                        rect_objects.append(new_rect)
                        object_tools[0].active = True
                        object_tools[1].active = False
                        object_tools[2].active = False
                        object_tools[0].tool_data = selected_object = [new_rect]
                    else:
                        selected_object = object_selector(selected_object, [mx, my])
                        if selected_object and object_tools[0].active:
                            selected_object[0].properties.append('no_move')
                        object_tools[0].tool_data = selected_object
                        object_tools[1].tool_data = selected_object
                        object_tools[2].tool_data = selected_object
                        ObjectStatUpdater(selected_object)
                        if object_tools[1].active:
                            velocity_mover = True
                        if object_tools[2].active:
                            size_mover = True
                        for tool in object_tools:
                            if tool.mouse_check():
                                if not tool.active:
                                    tool.active = True
                                    if (tool == object_tools[1]) and \
                                            (object_tools[0].active or object_tools[2].active):
                                        if object_tools[0].tool_data:
                                            if 'no_move' in object_tools[0].tool_data[0].properties:
                                                object_tools[0].tool_data[0].properties.remove('no_move')
                                        object_tools[0].tool_data = []
                                        object_tools[0].active = False
                                        object_tools[2].tool_data = []
                                        object_tools[2].active = False
                                    elif (tool == object_tools[0]) and \
                                            (object_tools[1].active or object_tools[2].active):
                                        object_tools[1].tool_data = []
                                        object_tools[1].active = False
                                        object_tools[2].tool_data = []
                                        object_tools[2].active = False
                                    elif (tool == object_tools[2]) and \
                                            (object_tools[0].active or object_tools[1].active):
                                        object_tools[0].tool_data = []
                                        object_tools[0].active = False
                                        object_tools[1].tool_data = []
                                        object_tools[1].active = False
                                else:
                                    if object_tools[0].tool_data:
                                        if 'no_move' in object_tools[0].tool_data[0].properties:
                                            object_tools[0].tool_data[0].properties.remove('no_move')
                                    object_tools[0].tool_data = []
                                    tool.active = False

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if Menu_state == field_menu:
                    for tool in field_tools:
                        if tool.active:
                            tool.active = False
                elif Menu_state == object_menu:
                    if object_tools[0].tool_data and object_tools[0].active:
                        try:
                            object_tools[0].tool_data[0].properties.remove('no_move')
                        except ValueError:
                            pass
                        object_tools[0].tool_data = []
                    elif object_tools[1].tool_data and object_tools[1].active:
                        velocity_mover = False
                    elif object_tools[2].tool_data and object_tools[2].active:
                        size_mover = False
                    for tool in object_tools:
                        if tool.mouse_check():
                            pass

    for tool in field_tools:
        tool.mouse_update()
    for tool in object_tools:
        tool.mouse_update(velocity_mover, size_mover)


def liquid_surface():
    gravity_angle = np.deg2rad(np.round(field_tools[0].tool_data))
    w, h = 1057, 636
    u, v = np.array([-np.sin(gravity_angle), -np.cos(gravity_angle)])
    a = 0.5 * (w - (h * u) / v)
    if (gravity_angle == 0) or (gravity_angle == np.pi):
        coord = [np.array([w/2 + 201, 2]), np.array([w/2 + 201, h + 2])]
    elif (gravity_angle == np.pi/2) or (gravity_angle == -np.pi/2):
        coord = [np.array([201, h/2 + 2]), np.array([w + 201, h/2 + 2])]
    else:
        if 0 <= a <= 1057:
            coord = [np.array([a + 201, 2]), np.array([w-a + 201, h + 2])]
        elif a < 0:
            coord = [np.array([201, abs(a/np.tan(gravity_angle)) + 2]),
                     np.array([w + 201, h - abs(a/np.tan(gravity_angle)) + 2])]
        else:
            coord = [np.array([w + 201, abs((a-w)/np.tan(gravity_angle)) + 2]),
                     np.array([201, h - abs((a-w)/np.tan(gravity_angle)) + 2])]
    orientation = 1 if -np.pi/2 < gravity_angle <= np.pi/2 else -1
    coord = coord[::orientation]
    vector = coord[0] - coord[1]
    length = np.linalg.norm(vector)

    def correction_vector(angle):
        corner_angle_1 = np.arctan(1057/636)
        corner_angle_2 = np.pi - corner_angle_1
        aa = a if np.sign(angle) == 1 else w - a
        angle = abs(angle)
        if 0 < angle < corner_angle_1:
            correction = abs(aa) * np.sin(angle)
        elif corner_angle_1 < angle < np.pi/2:
            correction = abs(aa / np.tan(angle)) * np.cos(angle)
        elif np.pi/2 < angle < corner_angle_2:
            correction = abs((aa-w)/np.tan(np.pi - angle)) * np.cos(np.pi - angle)
        elif corner_angle_2 < angle < np.pi:
            correction = abs(w-aa) * np.sin(np.pi - angle)
        else:
            correction = 0
        return abs(correction)

    correction_length = correction_vector(gravity_angle)
    front_point = (vector * correction_length) / length + coord[0]
    end_point = -(vector * correction_length) / length + coord[1]
    new_vector = front_point - end_point
    new_length = np.linalg.norm(new_vector)
    liquid_height = new_length - (field_tools[8].tool_data * new_length) / 100
    liquid_surface_point = (new_vector * liquid_height) / new_length + end_point

    sign = int(np.sign(gravity_angle))
    if 0 < abs(gravity_angle) < np.pi/2:
        top = [[201, 2],  [1258, 2]][::sign][0]
        bottom = [[1258, 638],  [201, 638]][::sign][0]
    elif np.pi/2 < abs(gravity_angle) < np.pi:
        top = [[201, 638], [1258, 638]][::sign][0]
        bottom = [[1258, 2], [201, 2]][::sign][0]
    elif gravity_angle == np.pi:
        top, bottom = [1258, 638], [201, 638]
    elif gravity_angle == np.pi/2:
        top, bottom = [201, 638], [201, 2]
    elif gravity_angle == -np.pi/2:
        top, bottom = [1258, 638], [1258, 2]
    else:
        top, bottom = [1258, 2], [201, 2]

    def intersection_point(line1, line2):
        l11, l12 = line1
        l21, l22 = line2
        x1, y1 = l11
        x2, y2 = l12
        x3, y3 = l21
        x4, y4 = l22
        p1_numerator = (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)
        denominator = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        p2_numerator = (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)
        return p1_numerator/denominator, p2_numerator/denominator

    if abs(gravity_angle) != np.pi/2:
        normal_line = [np.array(top) - front_point + liquid_surface_point, liquid_surface_point]
        int_left = intersection_point(normal_line, [[201, 2], [201, 638]])
        if 2 <= int_left[1] <= 638:
            intersect1 = int_left
        else:
            if int_left[1] < 2:
                intersect1 = intersection_point(normal_line, [[201, 2], [1258, 2]])
            else:
                intersect1 = intersection_point(normal_line, [[201, 638], [1258, 638]])
        int_right = intersection_point(normal_line, [[1258, 2], [1258, 638]])
        if 2 <= int_right[1] <= 638:
            intersect2 = int_right
        else:
            if int_right[1] < 2:
                intersect2 = intersection_point(normal_line, [[201, 2], [1258, 2]])
            else:
                intersect2 = intersection_point(normal_line, [[201, 638], [1258, 638]])
    else:
        intersect1, intersect2 = [liquid_surface_point[0], 2], [liquid_surface_point[0], 638]
    return intersect1, intersect2, top, bottom


def draw_liquid(screen):
    if field_tools[8].tool_data == 0:
        return None
    surface_l, surface_r, submerged, above = liquid_surface()
    surface_l = np.round(surface_l).astype(int)
    surface_r = np.round(surface_r).astype(int)
    other_corner_1 = [submerged[0], above[1]]
    other_corner_2 = [above[0], submerged[1]]
    if np.deg2rad(np.round(field_tools[0].tool_data)) in [0, np.pi, np.pi/2, -np.pi/2]:
        points = [surface_l, surface_r, submerged, above]
    elif submerged == [1258, 638]:
        if (surface_l[1] == 638) and (surface_r[0] == 1258):
            points = [submerged, surface_l, surface_r]
        elif (surface_l[1] == 638) and (surface_r[1] == 2):
            points = [submerged, surface_l, surface_r, other_corner_1]
        elif (surface_l[0] == 201) and (surface_r[0] == 1258):
            points = [submerged, other_corner_2, surface_l, surface_r]
        else:
            points = [submerged, other_corner_2, surface_l, surface_r, other_corner_1]
    elif submerged == [201, 638]:
        if (surface_l[0] == 201) and (surface_r[1] == 638):
            points = [submerged, surface_l, surface_r]
        elif (surface_l[0] == 201) and (surface_r[0] == 1258):
            points = [submerged, surface_l, surface_r, other_corner_2]
        elif (surface_l[1] == 2) and (surface_r[1] == 638):
            points = [submerged, other_corner_1, surface_l, surface_r]
        else:
            points = [submerged, other_corner_1, surface_l, surface_r, other_corner_2]
    elif submerged == [201, 2]:
        if (surface_l[0] == 201) and (surface_r[1] == 2):
            points = [submerged, surface_l, surface_r]
        elif (surface_l[0] == 201) and (surface_r[0] == 1258):
            points = [submerged, surface_l, surface_r, other_corner_2]
        elif (surface_l[1] == 638) and (surface_r[1] == 2):
            points = [submerged, other_corner_1, surface_l, surface_r]
        else:
            points = [submerged, other_corner_1, surface_l, surface_r, other_corner_2]
    else:
        if (surface_l[1] == 2) and (surface_r[0] == 1258):
            points = [submerged, surface_l, surface_r]
        elif (surface_l[0] == 201) and (surface_r[0] == 1258):
            points = [submerged, other_corner_2, surface_l, surface_r]
        elif (surface_l[1] == 2) and (surface_r[1] == 638):
            points = [submerged, surface_l, surface_r, other_corner_1]
        else:
            points = [submerged, other_corner_2, surface_l, surface_r, other_corner_1]
    points_list = [[np.round(x).astype(int), np.round(y).astype(int)] for [x, y] in points]
    pg.draw.polygon(screen, (131, 215, 238), points_list)


def Screen_Loader(screen):
    screen.fill((255, 255, 255))
    screen.blit(border, (0, 0))
    screen.blit(Menu_state, (0, 0))
    screen.blit(Sim_state, (11, 12))
    draw_liquid(screen)

    for circ in circle_objects:
        circ.draw(screen)
    for rect in rect_objects:
        rect.draw(screen)

    if Menu_state == field_menu:
        for tool in field_tools:
            tool.draw(screen)
    elif Menu_state == object_menu:
        for tool in object_tools:
            tool.draw(screen)


def update_simulator():
    if Sim_state == play:
        if len(circle_objects) > 1:
            combos = combinations(circle_objects, 2)
            for pair in combos:
                Cc.pair_forces_circles(pair, field_tools)
                Cc.circle_collisions(pair)
        for circle in circle_objects:
            if np.linalg.norm(circle.velocity) > 2000:
                circle_objects.remove(circle)
            Cc.forces_circles(circle, field_tools, liquid_surface)
            circle.update_center()
            circle.wall_collisions()
        if len(rect_objects) > 1:
            combos = combinations(rect_objects, 2)
            for pair in combos:
                Rc.pair_forces_rectangles(pair, field_tools)
                Rc.rectangle_collisions(pair, Screen)
        for rect in rect_objects:
            rect.wall_collisions()
            Rc.forces_rectangles(rect, field_tools)
            rect.update_corners()


if __name__ == '__main__':
    while True:
        Screen_Loader(Screen)
        user_input()
        update_simulator()
        pg.display.update()
        clock.tick(120)
