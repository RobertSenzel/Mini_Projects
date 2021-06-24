import numpy as np
import pygame as pg


class Rectangle:
    def __init__(self, corners, velocity, colour, density, charge, properties, e=1.0, rotate=0):
        self.corners = np.array([np.array(x) for x in corners])
        self.velocity = np.array(velocity, float)
        self.colour = colour
        self.density = density
        self.charge = charge
        self.rotate = rotate
        self.e = e
        self.properties = properties

    def update_corners(self):
        if 'no_move' not in self.properties:
            h, k, = self.velocity
            x, y, = self.center()
            a = self.rotate if 'rotate' in self.properties else 0
            matrix = np.array([[np.cos(a), -np.sin(a), h - x * np.cos(a) + y * np.sin(a) + x],
                               [np.sin(a), np.cos(a), k - x * np.sin(a) - y * np.cos(a) + y],
                               [0, 0, 1]])
            self.corners = np.dot(matrix, self.corners.T).T

    @staticmethod
    def shape():
        return 'rect'

    def draw(self, screen):
        draw_corners = [list(np.delete(x, 2)) for x in self.corners]
        pg.draw.polygon(screen, self.colour, draw_corners)

    def size(self):
        side1 = np.linalg.norm(np.array(self.corners[0]) - np.array(self.corners[1]))
        side2 = np.linalg.norm(np.array(self.corners[0]) - np.array(self.corners[-1]))
        return [side1, side2] if side1 > side2 else [side2, side1]

    def center(self):
        x1, y1, z1 = self.corners[0]
        x2, y2, z1 = self.corners[2]
        return [(x1+x2)/2, (y1+y2)/2]

    def area(self):
        length, width = self.size()
        return length * width

    def mass(self):
        return self.density * self.area()

    def inertia(self):
        l, w = self.size()
        return (1/12)*self.mass()*(l**2+w**2)

    def update_velocity(self, acceleration):
        if 'no_move' not in self.properties:
            self.velocity += acceleration

    def update_rotation(self, omega):
        if 'no_move' not in self.properties:
            self.rotate += omega

    def offset(self, vertex, norm):
        if list(norm) == [0.0, 1.0, 0.0]:
            end_index = 'top'
        elif list(norm) == [0.0, -1.0, 0.0]:
            end_index = 'bottom'
        elif list(norm) == [1.0, 0.0, 0.0]:
            end_index = 'left'
        else:
            end_index = 'right'
        endpoint = {'top': 2, 'bottom': 638, 'left': 201, 'right': 1258}
        vertex_index = 1 if endpoint[end_index] in [2, 638] else 0
        offset = abs(endpoint[end_index] - vertex[vertex_index])
        translate = np.array([[1, 0, offset*norm[0]], [0, 1, offset*norm[1]], [0, 0, 1]])
        self.corners = np.dot(translate, self.corners.T).T

    def check_collision(self):
        no_corner = False
        side = self.corners[1] - self.corners[0]
        if np.dot(np.array([1.0, 0.0, 0.0]), side) == 0 or np.dot(np.array([0.0, 1.0, 0.0]), side) == 0:
            no_corner = True
        for i, corner in enumerate(self.corners):
            if corner[0] < 201:
                if not no_corner:
                    return corner, np.array([1.0, 0.0, 0.0])
                else:
                    return np.array([corner[0], self.center()[1], 1]), np.array([1.0, 0.0, 0.0])
            elif corner[0] > 1258:
                if not no_corner:
                    return corner, np.array([-1.0, 0.0, 0.0])
                else:
                    return np.array([corner[0], self.center()[1], 1]), np.array([-1.0, 0.0, 0.0])
            elif corner[1] < 2:
                if not no_corner:
                    return corner, np.array([0.0, 1.0, 0.0])
                else:
                    return np.array([self.center()[0], corner[1], 1]), np.array([0.0, 1.0, 0.0])
            elif corner[1] > 638:
                if not no_corner:
                    return corner, np.array([0.0, -1.0, 0.0])
                else:
                    return np.array([self.center()[0], corner[1], 1]), np.array([0.0, -1.0, 0.0])
        return 0, 0

    def wall_collisions(self):
        corner, n = self.check_collision()
        if type(n) != int:
            self.offset(corner, n)
            v = np.append(self.velocity, 0)
            w = np.array([0, 0, self.rotate])
            Rap = corner - np.append(self.center(), 1)
            mass = self.mass()
            inertia = self.inertia()
            rn = np.cross(Rap, n)

            Vap1 = v + np.cross(w, Rap)
            impulse = (-(1+self.e)*np.dot(Vap1, n))/((1/mass) + (np.dot(rn, rn))/inertia)

            vf = v + impulse*n/mass
            self.velocity = vf[:2]
            wf = w + np.cross(Rap, impulse*n)/inertia
            self.rotate = wf[2]


def forces_rectangles(rect, field_tools):
    gravity_angle = np.deg2rad(np.round(field_tools[0].tool_data))
    gravity_magnitude = field_tools[2].tool_data / 100
    gravity = gravity_magnitude * np.array([-np.sin(gravity_angle), -np.cos(gravity_angle)])

    electric_angle = np.deg2rad(np.round(field_tools[1].tool_data))
    electric_magnitude = field_tools[3].tool_data * 1000
    electric = electric_magnitude * np.array([-np.sin(electric_angle), -np.cos(electric_angle)])
    rect.update_velocity(gravity + (rect.charge / rect.mass()) * electric)


def rectangle_collisions(pair, screen):
    rect1, rect2 = pair
    rad1 = np.linalg.norm(rect1.corners[0][:2] - rect1.center())
    rad2 = np.linalg.norm(rect2.corners[0][:2] - rect2.center())

    def translate(vec, coord):
        h, k = vec[:2]
        trans = np.array([[1, 0, h], [0, 1, k], [0, 0, 1]])
        return np.dot(trans, coord.T).T

    def collision_detect(rect1_corners, rect2_corners):
        u = rect1_corners[1] - rect1_corners[0]
        a = -np.arctan(u[1]/u[0]) if int(u[0]) != 0 else 0
        h, k = -rect1_corners[0][:2]
        matrix = np.array([[np.cos(a), -np.sin(a), h * np.cos(a) - k * np.sin(a)],
                           [np.sin(a), np.cos(a), h * np.sin(a) + k * np.cos(a)],
                           [0, 0, 1]])
        new_rect1 = np.dot(matrix, rect1_corners.T).T
        new_rect2 = np.dot(matrix, rect2_corners.T).T
        orient = 1 if new_rect1[0][0] == new_rect1[1][0] else -1
        collected_data = []

        def check_center(corners):
            x1, y1, z1 = corners[0]
            x2, y2, z1 = corners[2]
            center = [(x1 + x2) / 2, (y1 + y2) / 2]
            c1a = new_rect1[0][0] <= center[0] <= new_rect1[-orient][0]
            c1b = new_rect1[0][0] >= center[0] >= new_rect1[-orient][0]
            c2a = new_rect1[0][1] <= center[1] <= new_rect1[orient][1]
            c2b = new_rect1[0][1] >= center[1] >= new_rect1[orient][1]
            c1 = c1a or c1b
            c2 = c2a or c2b
            if c1 and c2:
                return True
            else:
                return False

        if check_center(new_rect2):
            print('stuck')
            return 'stuck'
        for i, corner in enumerate(new_rect2):
            con1a = new_rect1[0][0] <= corner[0] <= new_rect1[-orient][0]
            con1b = new_rect1[0][0] >= corner[0] >= new_rect1[-orient][0]
            con2a = new_rect1[0][1] <= corner[1] <= new_rect1[orient][1]
            con2b = new_rect1[0][1] >= corner[1] >= new_rect1[orient][1]
            con1 = con1a or con1b
            con2 = con2a or con2b
            if con1 and con2:
                dists = [abs(corner[0]), abs(new_rect1[-orient][0]-corner[0]),
                         abs(corner[1]), abs(new_rect1[orient][1]-corner[1])]

                rotate = np.array([[np.cos(-a), -np.sin(-a), 0], [np.sin(-a), np.cos(-a), 0], [0, 0, 1]])
                axes = [np.array([-1, 0, 1]), np.array([1, 0, 1]), np.array([0, -1, 1]), np.array([0, 1, 1])]
                correct = 1 if con1a else -1
                norm = np.dot(rotate, axes[dists.index(min(dists))])
                collected_data.append([rect2_corners[i], norm*correct, min(dists)])
        if len(collected_data) == 1:
            return collected_data[0]
        elif len(collected_data) == 2:
            p1, p2 = collected_data[0][0], collected_data[1][0]
            collected_data[0][0] = np.array([(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, 1])
            return collected_data[0]
        else:
            return []

    if np.linalg.norm(np.array(rect1.center()) - np.array(rect2.center())) > rad1 + rad2:
        data = []
    else:
        data1 = collision_detect(rect1.corners, rect2.corners)
        data2 = collision_detect(rect2.corners, rect1.corners)
        if data1 == 'stuck':
            data = []
            vec = np.array(rect1.center()) - np.array(rect2.center())
            rect1.corners = translate(vec, rect1.corners)
        elif data2 == 'stuck':
            data = []
            vec = np.array(rect2.center()) - np.array(rect1.center())
            rect1.corners = translate(vec, rect1.corners)
        elif data1 and not data2:
            data = data1
            data.append(rect2)
            data.append(rect1)
        elif data2 and not data1:
            data = data2
            data.append(rect1)
            data.append(rect2)
        elif data1 and data2:
            data1[0] = np.array([(data1[0][0]+data2[0][0])/2, (data1[0][1]+data2[0][1])/2, 1])
            data = data1
            data.append(rect2)
            data.append(rect1)
        else:
            data = []
    if data:
        point, n, corr, rec1, rec2 = data
        point = np.round(point)
        n = np.round(n, 3)
        # corr += 1

        unin = n[:2]/np.linalg.norm(n[:2])
        correction1, correction2 = (corr/2) * unin, (-corr/2) * unin
        rec1.corners = translate(correction1, rec1.corners)
        rec2.corners = translate(correction2, rec2.corners)
        point = translate(correction1, point)
        # pg.draw.circle(screen, (0, 200, 0), point[:2].astype(int), 5)
        # pg.draw.line(screen, (0, 0, 0), point[:2].astype(int), (point[:2] + 20*unin).astype(int))
        R1 = point[:2] - rec1.center()
        R2 = point[:2] - rec2.center()
        v1 = np.append(rec1.velocity, 0)
        v2 = np.append(rec2.velocity, 0)
        w1 = np.array([0, 0, rec1.rotate])
        w2 = np.array([0, 0, rec2.rotate])
        Vp1 = v1 + np.cross(w1, R1)
        Vp2 = v2 + np.cross(w2, R2)
        m1 = rec1.mass()
        m2 = rec2.mass()
        I1 = rec1.inertia()
        I2 = rec2.inertia()

        Vab = Vp1 - Vp2
        e = (rec1.e+rec2.e)/2
        rn1 = np.cross(R1, n)
        rn2 = np.cross(R2, n)

        impulse = (-(1 + e) * np.dot(Vab, n)) / \
                  ((1 / m1) + (1 / m2) + (np.dot(rn1, rn1)) / I1 + (np.dot(rn2, rn2)) / I2)

        vf1 = v1 + impulse * n / m1
        vf2 = v2 - impulse * n / m2
        rec1.velocity = vf1[:2]
        rec2.velocity = vf2[:2]

        wf1 = w1 + np.cross(R1, impulse * n) / I1
        wf2 = w2 - np.cross(R2, impulse * n) / I2
        rec1.rotate = wf1[2]
        rec2.rotate = wf2[2]


def pair_forces_rectangles(pair, field_tools):
    rect1, rect2 = pair
    G = field_tools[4].tool_data
    E = field_tools[5].tool_data
    vector = np.array(rect1.center()[:2]) - np.array(rect2.center()[:2])
    dist = np.linalg.norm(vector)

    g_force = (1e-5 * G * rect1.mass() * rect2.mass() / dist ** 3) * vector
    g_acc1 = -g_force / rect1.mass()
    g_acc2 = g_force / rect2.mass()

    e_force = (1e8 * E * rect1.charge * rect2.charge / dist ** 3) * vector
    e_acc1 = e_force / rect1.mass()
    e_acc2 = -e_force / rect2.mass()

    rect1.update_velocity(g_acc1 + e_acc1)
    rect2.update_velocity(g_acc2 + e_acc2)
