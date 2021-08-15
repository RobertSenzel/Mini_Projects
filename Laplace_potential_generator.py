import sys
import numba
import numpy as np
import pygame as pg
import pyautogui as pag


def draw_graph_pygame(potential, gradient_toggled, cmap, graph3d_data):
    """ converts matplotlib figure to an image """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.backends.backend_agg as agg
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from mpl_toolkits.mplot3d import Axes3D

    if not graph3d_data[0]:
        fig = plt.figure(figsize=(9, 9), dpi=100)
        fig.patch.set_facecolor('black')
        ax = fig.gca()
        edge = np.linspace(0, 299, 300)
        xv, yv = np.meshgrid(edge, edge)
        c_plot = ax.contourf(xv, yv, potential, 50, cmap=cmap)
        if np.sum(potential) and gradient_toggled:
            skip = slice(None, None, 15)
            g = np.gradient(-potential[skip, skip].T, edge[skip], edge[skip])
            ax.quiver(xv[skip, skip], yv[skip, skip], g[0].T, g[1].T, scale=0.9)

        def color_bar(mappable):
            last_axes = plt.gca()
            divider = make_axes_locatable(mappable.axes)
            cax = divider.append_axes('bottom', size='5%', pad='5%')
            c_bar = ax.figure.colorbar(mappable, cax=cax, orientation='horizontal')
            c_bar.ax.tick_params(axis='both', colors='white')
            plt.sca(last_axes)
            return c_bar

        color_bar(c_plot)
        ax.tick_params(axis='both', colors='white')
        ax.set_aspect('equal')
    else:
        fig = plt.figure(figsize=(9, 9), dpi=100)
        ax = Axes3D(fig)
        ax.set_facecolor('black')
        edge = np.linspace(0, 299, 300)
        xv, yv = np.meshgrid(edge, edge)
        ax.plot_surface(xv, yv, potential, cmap=cmap, linewidth=0, antialiased=False)
        ax.view_init(elev=graph3d_data[2], azim=graph3d_data[1])

    canvas = agg.FigureCanvasAgg(fig)
    plt.close(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return pg.image.fromstring(raw_data, (900, 900), 'RGB')


@numba.jit('f8[:,:](f8[:,:], b1[:,:], i8)', nopython=True, nogil=True)
def compute_potential(potential, fixed_bool, n_iter):
    """ solving Laplace's equation using finite difference method"""
    length = len(potential[0])
    for n in range(n_iter):
        for i in range(1, length-1):
            for j in range(1, length-1):
                if not (fixed_bool[i][j]):
                    potential[i][j] = 1/4*(potential[i+1][j] + potential[i-1][j] + potential[i][j+1] + potential[i][j-1])
    return potential


def convert_point(point):
    """ change from window coordinate system to that of the graph """
    mx, my = point
    coord_x = int((mx - 148) / 630 * 300)
    coord_y = int((739 - my) / 629 * 300)
    return coord_x, coord_y


def kernel(x, y):
    return [[x, y + 2],
            [x + 1, y + 1], [x, y + 1], [x - 1, y + 1],
            [x + 2, y], [x + 1, y], [x, y], [x - 1, y], [x - 2, y],
            [x + 1, y - 1], [x, y - 1], [x - 1, y - 1],
            [x, y - 2]]


class TestCharge:
    def __init__(self, pos, color, radius, velocity, alpha):
        self.pos = pos
        self.color = color
        self.rad = radius
        self.vel = velocity
        self.alpha = alpha   # acceleration = -alpha * gradient

    def draw_ball(self, screen):
        pg.draw.circle(screen, self.color, np.round(self.pos).astype(int), self.rad)

    def update_vel(self, gradient):
        px, py = convert_point(self.pos)
        px, py = min(max(px, 0), 299), min(max(py, 0), 299)
        gx, gy = gradient[0][int(py), int(px)], gradient[1][int(py), int(px)]
        self.vel += self.alpha * np.array([gx, -gy])

    def update_pos(self):
        self.pos += self.vel


class Controller:
    def __init__(self):
        self.potential = np.zeros((300, 300))
        self.toggle_gradient = 0
        self.graph3d = [False, 0, 45]
        self.cmap_i = 0
        self.colour_maps = ['terrain', 'viridis', 'inferno', 'plasma', 'gist_earth', 'ocean', 'Set1', 'hot', 'cool',
                            'gist_heat', 'tab20b', 'hsv', 'spring', 'summer', 'autumn', 'winter', 'binary', 'bone', 'prism']
        self.graph = self.draw_graph()
        self.input_potential_bool = np.zeros((300, 300))
        self.input_potential_values = np.zeros((300, 300))
        self.gradient = [np.zeros(300), np.zeros(300)]

    def set_boundary(self):
        bounds = np.ones(300)
        self.potential[0, :] = bounds
        self.potential[-1, :] = bounds
        self.potential[:, 0] = bounds
        self.potential[:, -1] = bounds

    def draw_graph(self):
        return draw_graph_pygame(self.potential, self.toggle_gradient, self.colour_maps[self.cmap_i], self.graph3d)

    def calculate(self):
        self.set_boundary()
        convert_to_bool = self.input_potential_bool.astype(bool)
        self.potential[convert_to_bool] = self.input_potential_values[convert_to_bool]
        self.potential = compute_potential(self.potential, convert_to_bool, 10000)
        self.graph = self.draw_graph()

    def draw_potential(self, point, value):
        dx, dy = convert_point(point)
        for i, j in kernel(dy, dx):
            i, j = min(max(i, 0), 299), min(max(j, 0), 299)
            self.input_potential_values[i, j] = value
            self.input_potential_bool[i, j] = 1

    def reset(self):
        self.potential = np.zeros((300, 300))
        self.graph = self.draw_graph()
        self.input_potential_bool = np.zeros((300, 300))

    def calculate_gradient(self):
        edge = np.linspace(0, 299, 300)
        gx, gy = np.gradient(-self.potential.T, edge, edge)
        self.gradient = [gx.T, gy.T]


def main():
    pg.init()
    width, height = (1200, 900)
    Screen = pg.display.set_mode((width, height))
    pg.display.set_caption('Laplace')
    win = pag.getWindowsWithTitle('Laplace')
    win[0].moveTo(60, 60)
    clock = pg.time.Clock()
    menu = pg.image.load('images\\laplace_menu.png').convert()
    font = pg.font.SysFont('consolas', size=25)
    control = Controller()
    drawn_potentials, test_charges = [], []
    draw, potential_input = False, 1.0
    while True:
        Screen.blit(control.graph, (0, 0))
        Screen.blit(menu, (900, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    draw = True
                elif event.button == 2:
                    potential_input *= -1
                elif event.button == 3:
                    test_charges.append(TestCharge(np.array(pg.mouse.get_pos()).astype(float), (0, 0, 0), 7,
                                                   np.array([0.0, 0.0]), 10))
                elif event.button == 4:
                    potential_input += 0.1
                elif event.button == 5:
                    potential_input -= 0.1

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    draw = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    control.calculate()
                    drawn_potentials.clear()
                elif event.key == pg.K_r:
                    control.reset()
                    drawn_potentials.clear()
                    test_charges.clear()
                elif event.key == pg.K_g:
                    control.toggle_gradient ^= 1
                    control.graph = control.draw_graph()
                elif event.key == pg.K_b:
                    test_charges.clear()
                elif event.key == pg.K_c:
                    control.cmap_i = control.cmap_i + 1 if control.cmap_i != len(control.colour_maps) - 1 else 0
                    control.graph = control.draw_graph()
                elif event.key == pg.K_x:
                    control.graph3d[0] ^= 1
                    control.graph = control.draw_graph()
                    test_charges.clear()
                    if not control.graph3d[0]:
                        control.graph3d = [0, 0, 45]
                elif event.key == pg.K_a:
                    control.graph3d[1] -= 30
                    control.graph = control.draw_graph()
                elif event.key == pg.K_d:
                    control.graph3d[1] += 30
                    control.graph = control.draw_graph()
                elif event.key == pg.K_w:
                    control.graph3d[2] += 15
                    control.graph = control.draw_graph()
                elif event.key == pg.K_s:
                    control.graph3d[2] -= 15
                    control.graph = control.draw_graph()

        if draw:
            control.draw_potential(pg.mouse.get_pos(), potential_input)
            drawn_potentials.append([pg.mouse.get_pos(), potential_input])
        for coords, val in drawn_potentials:
            color = (255, 255, 255) if np.sign(val) == 1 else (0, 0, 0)
            pg.draw.circle(Screen, color, coords, 5)
        for ball in test_charges:
            control.calculate_gradient()
            ball.update_vel(control.gradient)
            ball.update_pos()
            ball.draw_ball(Screen)

        potential_input = min(max(potential_input, -1.0), 1.0)
        tool_text = font.render(f'Input potential: {round(potential_input, 1)}, '
                                f'cmap: {control.colour_maps[control.cmap_i]}',
                                True, (150, 150, 150))
        tool_text_rect = tool_text.get_rect(center=(450, 50))
        Screen.blit(tool_text, tool_text_rect)
        pg.display.update()

        def fps():
            if draw: return 200
            elif control.graph3d[0]: return 5
            else: return 30

        clock.tick(fps())


if __name__ == '__main__':
    main()

