import numpy as np
import pygame as pg


class Circle:
    def __init__(self, center, velocity, colour, radius, density, charge, rotate, properties):
        self.center = np.array(center).astype(float)
        self.velocity = np.array(velocity).astype(float)
        self.colour = colour
        self.radius = radius if radius > 0 else 1
        self.density = density
        self.charge = charge
        self.rotate = rotate
        self.properties = properties

    @staticmethod
    def shape():
        return 'circle'

    def properties_check(self, prop):
        return prop in self.properties

    def mass(self):
        return self.density * np.pi * self.radius ** 2

    def update_center(self):
        if 'no_move' not in self.properties:
            self.center += self.velocity

    def update_velocity(self, acceleration):
        if 'no_move' not in self.properties:
            self.velocity += acceleration

    def draw(self, screen):
        pg.draw.circle(screen, self.colour, np.round(self.center).astype(int), self.radius)

    def wall_collisions(self):
        x, y = self.center
        width, height = np.array([1260.0, 640.0]) - np.array([2.0, 2.0])
        if y >= height - self.radius:
            self.center *= (1.0, 0.0)
            self.center += (0.0, height - self.radius)
            self.velocity *= (1.0, -1.0)
        if y <= 1 + self.radius:
            self.center *= (1.0, 0)
            self.center += (0.0, 1.0 + self.radius)
            self.velocity *= (1.0, -1.0)
        if x <= 201 + self.radius:
            self.center *= (0.0, 1.0)
            self.center += (201.0 + self.radius, 0.0)
            self.velocity *= (-1.0, 1.0)
        if x >= width - self.radius:
            self.center *= (0.0, 1.0)
            self.center += (width - self.radius, 0.0)
            self.velocity *= (-1.0, 1.0)


def circle_collisions(pair):
    # redo with impulse
    circle1, circle2 = pair
    distance = np.linalg.norm(circle2.center - circle1.center)
    if ('ghost' in circle1.properties) or ('ghost' in circle2.properties):
        return
    if distance <= circle1.radius + circle2.radius:
        overlap = ((circle1.radius + circle2.radius - distance) / 2) * ((circle2.center - circle1.center) / distance)
        circle1.center -= overlap
        circle2.center += overlap
        m1, m2 = circle1.mass(), circle2.mass()

        u1, u2 = circle1.velocity, circle2.velocity
        c1, c2 = circle1.center, circle2.center

        norm1 = np.linalg.norm(c1 - c2) ** 2
        norm2 = np.linalg.norm(c2 - c1) ** 2

        circle1.velocity = (u1 - (((2 * m2) / (m1 + m2)) * np.dot(u1 - u2, c1 - c2) / norm1) * (c1 - c2))
        circle2.velocity = (u2 - (((2 * m1) / (m1 + m2)) * np.dot(u2 - u1, c2 - c1) / norm2) * (c2 - c1))


def pair_forces_circles(pair, field_tools):
    circle1, circle2 = pair
    G = field_tools[4].tool_data
    E = field_tools[5].tool_data
    vector = circle1.center - circle2.center
    dist = np.linalg.norm(vector)

    g_force = (1e-5 * G * circle1.mass() * circle2.mass() / dist ** 3) * vector
    g_acc1 = -g_force / circle1.mass()
    g_acc2 = g_force / circle2.mass()

    e_force = (1e8 * E * circle1.charge * circle2.charge / dist ** 3) * vector
    e_acc1 = e_force / circle1.mass()
    e_acc2 = -e_force / circle2.mass()

    circle1.update_velocity(g_acc1 + e_acc1)
    circle2.update_velocity(g_acc2 + e_acc2)


def submerged_circle(circle, field_tools, liquid_surface):
    if field_tools[8].tool_data == 0:
        return 0
    area = np.pi * circle.radius ** 2
    gravity_angle = np.deg2rad(np.round(field_tools[0].tool_data))
    surface_l, surface_r, lower, higher = liquid_surface()
    x1, y1 = surface_l
    x2, y2 = surface_r
    a, b = circle.center
    denominator = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if float(denominator) == 0.0:
        distance = 0
    else:
        distance = ((x2 - x1) * (y1 - b) - (x1 - a) * (y2 - y1)) / denominator

    sign = int(np.sign(distance))
    if float(distance) == 0.0:
        return area/2
    elif -np.pi/2 <= gravity_angle < np.pi/2:
        submerged = True if sign == 1 else False
    else:
        submerged = True if sign == -1 else False
    if (circle.radius <= abs(distance)) and not submerged:
        return 0
    elif (circle.radius <= abs(distance)) and submerged:
        return area
    else:
        arc_area = circle.radius ** 2 * np.arccos(np.abs(distance) / circle.radius)
        triangle_area = np.sqrt(circle.radius ** 2 - abs(distance) ** 2) * np.abs(distance)
        if not submerged:
            return arc_area - triangle_area
        else:
            return area - arc_area + triangle_area


def forces_circles(circle, field_tools, liquid_surface):
    gravity_angle = np.deg2rad(np.round(field_tools[0].tool_data))
    gravity_magnitude = field_tools[2].tool_data / 100
    gravity = gravity_magnitude * np.array([-np.sin(gravity_angle), -np.cos(gravity_angle)])

    electric_angle = np.deg2rad(np.round(field_tools[1].tool_data))
    electric_magnitude = field_tools[3].tool_data * 1000
    electric = electric_magnitude * np.array([-np.sin(electric_angle), -np.cos(electric_angle)])

    air_coeff = field_tools[6].tool_data
    liquid_coeff = field_tools[7].tool_data
    speed = np.linalg.norm(circle.velocity)
    liquid_height = (field_tools[8].tool_data * 636) / 100
    if float(speed) != 0.0:
        unit = circle.velocity / speed
        air_resistance = 0.1 * -np.pi * air_coeff * circle.radius * speed ** 2 * unit

        if submerged_circle(circle, field_tools, liquid_surface) > 0:
            liquid_resistance = 0.2 * -np.pi * liquid_coeff * circle.radius * speed ** 2 * unit
        else:
            liquid_resistance = 0
    else:
        air_resistance = 0
        liquid_resistance = 0
    if float(liquid_height) != 0.0:
        unit = np.array([np.sin(gravity_angle), np.cos(gravity_angle)])
        buoyancy_force = liquid_coeff * gravity_magnitude * submerged_circle(circle, field_tools, liquid_surface) * unit
    else:
        buoyancy_force = 0
    circle.update_velocity(gravity + (circle.charge / circle.mass()) * electric
                           + air_resistance / circle.mass() + liquid_resistance / circle.mass()
                           + buoyancy_force / circle.mass())

