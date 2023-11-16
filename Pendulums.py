import sys
import numpy as np
import pyautogui as pag
import pygame as pg
import tkinter as tk
from sympy import symbols, sympify, lambdify
from sympy.physics.mechanics import dynamicsymbols, ReferenceFrame, Point, inertia, RigidBody, KanesMethod
from pydy.codegen.ode_function_generators import generate_ode_function
from scipy.integrate import odeint


def mass_matrix_save(n):
    n2 = 'Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, Iz_1 + Iz_2 + cml_1**2*m_1 + ' \
         'm_2*(L_1**2 + 2*L_1*cml_2*cos(th_2(t)) + cml_2**2), Iz_2 + cml_2*m_2*(L_1*cos(th_2(t)) + ' \
         'cml_2)], [0, 0, Iz_2 + cml_2*m_2*(L_1*cos(th_2(t)) + cml_2), Iz_2 + cml_2**2*m_2]])'

    n3 = 'Matrix([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, Iz_1 + Iz_2 + ' \
         'Iz_3 + cml_1**2*m_1 + m_2*(L_1**2 + 2*L_1*cml_2*cos(th_2(t)) + cml_2**2) + ' \
         'm_3*(L_1**2 + 2*L_1*L_2*cos(th_2(t)) + 2*L_1*cml_3*cos(th_2(t) + th_3(t)) + L_2**2 + ' \
         '2*L_2*cml_3*cos(th_3(t)) + cml_3**2), Iz_2 + Iz_3 + cml_2*m_2*(L_1*cos(th_2(t)) + cml_2) + ' \
         'm_3*(L_1*L_2*cos(th_2(t)) + L_1*cml_3*cos(th_2(t) + th_3(t)) + L_2**2 + 2*L_2*cml_3*cos(th_3(t)) + ' \
         'cml_3**2), Iz_3 + cml_3*m_3*(L_1*cos(th_2(t) + th_3(t)) + L_2*cos(th_3(t)) + cml_3)], ' \
         '[0, 0, 0, Iz_2 + Iz_3 + cml_2*m_2*(L_1*cos(th_2(t)) + cml_2) + m_3*(L_1*L_2*cos(th_2(t)) + ' \
         'L_1*cml_3*cos(th_2(t) + th_3(t)) + L_2**2 + 2*L_2*cml_3*cos(th_3(t)) + cml_3**2), Iz_2 + ' \
         'Iz_3 + cml_2**2*m_2 + m_3*(L_2**2 + 2*L_2*cml_3*cos(th_3(t)) + cml_3**2), Iz_3 + ' \
         'cml_3*m_3*(L_2*cos(th_3(t)) + cml_3)], [0, 0, 0, Iz_3 + cml_3*m_3*(L_1*cos(th_2(t) + ' \
         'th_3(t)) + L_2*cos(th_3(t)) + cml_3), Iz_3 + cml_3*m_3*(L_2*cos(th_3(t)) + cml_3), Iz_3 + cml_3**2*m_3]])'

    pends = [0, 0, n2, n3]
    return sympify(pends[n])


def draw_graph_pygame(x_data, y_data, size, n_p):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.backends.backend_agg as agg
    import pylab
    from seaborn import set_style
    set_style('darkgrid')

    limits = [[-n_p * 3 - 1, n_p * 3 + 1], [-n_p * 3 - 1, n_p * 3 + 1]]

    fig = pylab.figure(figsize=[int(size[0] / 100), int(size[1] / 100)], dpi=100)
    fig.patch.set_facecolor('xkcd:grey blue')
    ax = fig.gca()
    ax.plot(x_data, y_data)
    ax.set_xlim(limits[0])
    ax.set_ylim(limits[1])

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return pg.image.fromstring(raw_data, size, "RGB")


def create_pend(NP, numerical_constants, final_time, x0, input_torques):
    g = symbols('g')

    frames = [ReferenceFrame(fr'fr_{i}') for i in range(NP + 1)]
    thetas = dynamicsymbols(', '.join([fr'th_{i + 1}' for i in range(NP)]))
    [frames[i + 1].orient(frames[i], 'Axis', (thetas[i], frames[i].z)) for i in range(NP)]

    points = [Point(fr'p_{i}') for i in range(NP + 1)]
    pend_lens = symbols(', '.join([fr'L_{i + 1}' for i in range(NP)]))
    [points[i + 1].set_pos(points[i], pend_lens[i] * frames[i + 1].y) for i in range(NP)]

    pend_com_lens = symbols(', '.join([fr'cml_{i + 1}' for i in range(NP)]))
    pend_coms = [Point(fr'cm_{i + 1}') for i in range(NP)]
    [pend_coms[i].set_pos(points[i], pend_com_lens[i] * frames[i + 1].y) for i in range(NP)]

    omegas = dynamicsymbols(', '.join([fr'om_{i + 1}' for i in range(NP)]))
    kinematical_differential_equations = [omegas[i] - thetas[i].diff() for i in range(NP)]

    [frames[i + 1].set_ang_vel(frames[i], omegas[i] * frames[i].z) for i in range(NP)]
    points[0].set_vel(frames[0], 0 * frames[0].z)
    [points[i + 1].v2pt_theory(points[i], frames[0], frames[i + 1]) for i in range(NP)]
    [pend_coms[i].v2pt_theory(points[i], frames[0], frames[i + 1]) for i in range(NP)]

    pend_mass = symbols(', '.join([fr'm_{i + 1}' for i in range(NP)]))
    pend_inertias = symbols(', '.join([fr'Iz_{i + 1}' for i in range(NP)]))

    pend_central_inertias = [(inertia(frames[i + 1], 0, 0, pend_inertias[i]), pend_coms[i]) for i in range(NP)]

    pends = [RigidBody(f'Pend_{i + 1}', pend_coms[i], frames[i + 1], pend_mass[i], pend_central_inertias[i]) for i in
             range(NP)]

    pend_grav_forces = [(pend_coms[i], -pend_mass[i] * g * frames[0].y) for i in range(NP)]

    p_torques = dynamicsymbols(', '.join([fr'T_{i + 1}' for i in range(NP)]))
    pend_torques = [(frames[i + 1], p_torques[i] * frames[0].z - p_torques[i + 1] * frames[0].z) for i in range(NP - 1)]
    pend_torques.append((frames[-1], p_torques[-1] * frames[0].z))

    # kane = KanesMethod(frames[0], thetas, omegas, kinematical_differential_equations)
    # loads = pend_grav_forces.copy()
    # loads.extend(pend_torques)
    # fr, frstar = kane.kanes_equations(pends, loads)
    # mass_matrix = trigsimp(kane.mass_matrix_full)
    # forcing_vector = trigsimp(kane.forcing_full)

    # above code works for n pendulums, two lines below are the optimized versions of n=2,3,4,5,6
    mass_matrix = mass_matrix_save(NP)
    forcing_vector = force_matrix_save(NP)
    constants = [[pend_lens[i], pend_com_lens[i], pend_mass[i], pend_inertias[i]] for i in range(NP)]
    constants = [item for sublist in constants for item in sublist]
    constants.append(g)

    right_hand_side = generate_ode_function(forcing_vector, thetas, omegas, constants, mass_matrix=mass_matrix,
                                            specifieds=p_torques)

    frames_per_sec = 24
    t = np.linspace(0, final_time, final_time * frames_per_sec)
    y = odeint(right_hand_side, x0, t, args=(input_torques, numerical_constants))

    p_coords = [points[i + 1].pos_from(points[0]).express(frames[0]).to_matrix(frames[0]).row_del(2) for i in range(NP)]
    variables = thetas.copy()
    variables.extend(pend_lens)
    p_funcs = [lambdify([variables], p_coords[i], 'numpy') for i in range(NP)]

    inputs = [x for x in y.T[:int(len(y[0]) / 2)]]
    pend_lens_num = np.array([numerical_constants[i*4] for i in range(NP)])
    inputs.extend([np.ones(len(t)) * pend_lens_num[i] for i in range(NP)])

    return [np.stack(p_funcs[i](inputs)[:2].tolist(), axis=1)[0].T for i in range(NP)]


def convert_point(point, n_p):
    if (point[0] > 50) or (point[1] > 50):
        return point
    mx, my = point
    x_limits, y_limits = [[-n_p * 3 - 1, n_p * 3 + 1], [-n_p * 3 - 1, n_p * 3 + 1]]
    xr = x_limits[1] - x_limits[0]
    yr = y_limits[1] - y_limits[0]
    xp, yp = 697, 694
    ze = (112 + xp / xr * abs(x_limits[0]), 801 - yp / yr * abs(y_limits[0]))
    return int(xp / xr * mx + ze[0]), int(-yp / yr * my + ze[1])


def find_angles(points):

    def rotate_m(ang, vector):
        R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        return np.dot(R, vector).T

    angles = []
    num = len(points)-1
    p = np.array([convert_point(x, num) for x in points])
    pre_vec = [np.array([0, -1])]
    for i in range(num):
        rot_vec = rotate_m((sum(angles) if angles else 0), p[i+1]-p[i])
        sign = 1 if 0 > rot_vec[0] else -1

        vec = np.dot(p[i+1]-p[i], pre_vec[i])/(np.linalg.norm(p[i+1]-p[i])*np.linalg.norm(pre_vec[i]))

        angles.append(sign * np.arccos(vec))
        pre_vec.append(p[i+1]-p[i])

    angles.extend([0]*num)
    return np.array(angles)


class Controller(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('300x900+960+60')
        self.grid()
        self.master.configure(bg='#6b8ba4')

        self.sim_state = tk.Button(self, text='play/pause', command=self.play_pause, bg='#929591', height=3, width=14)
        self.reset = tk.Button(self, text='reset', command=self.reset, bg='#929591', height=3, width=14)
        self.calc = tk.Button(self, text='calculate', command=self.calculate, bg='#929591', height=3, width=14)

        self.sim_state.grid(column=0, row=0, columnspan=3, rowspan=2)
        self.reset.grid(column=3, row=0, columnspan=3, rowspan=2)
        self.calc.grid(column=0, row=3, columnspan=3, rowspan=2)

        self.var = tk.IntVar(value=0)
        self.rad = self.radio_button()

        self.data = []
        self.time = 0
        self.play = 0
        self.graph = draw_graph_pygame(np.array([]), np.array([]), (900, 900),  self.var.get())
        self.init = []
        self.init_coords = []
        self.rod_density = 0.333

    def play_pause(self):
        self.play ^= 1

    def reset(self):
        self.play, self.time, self.data = 0, 0, 0

    def radio_button(self):
        radio_b = tk.Radiobutton(self, text="1", variable=self.var, value=1, command=self.init_pend, bg='#929591')
        radio_b.grid(column=3, row=3, sticky=tk.N+tk.E+tk.S+tk.W)
        radio_b = tk.Radiobutton(self, text="2", variable=self.var, value=2, command=self.init_pend, bg='#929591')
        radio_b.grid(column=4, row=3, sticky=tk.N+tk.E+tk.S+tk.W)
        radio_b = tk.Radiobutton(self, text="3", variable=self.var, value=3, command=self.init_pend, bg='#929591')
        radio_b.grid(column=5, row=3, sticky=tk.N+tk.E+tk.S+tk.W)
        radio_b = tk.Radiobutton(self, text="4", variable=self.var, value=4, command=self.init_pend, bg='#929591')
        radio_b.grid(column=3, row=4, sticky=tk.N+tk.E+tk.S+tk.W)
        radio_b = tk.Radiobutton(self, text="5", variable=self.var, value=5, command=self.init_pend, bg='#929591')
        radio_b.grid(column=4, row=4, sticky=tk.N+tk.E+tk.S+tk.W)
        radio_b = tk.Radiobutton(self, text="6", variable=self.var, value=6, command=self.init_pend, bg='#929591')
        radio_b.grid(column=5, row=4, sticky=tk.N+tk.E+tk.S+tk.W)
        return radio_b

    def calculate(self):
        self.play, self.time, self.data = 0, 0, 0
        n_p = self.var.get()
        if n_p:
            self.init[1] = find_angles(self.init_coords)
            self.data = create_pend(self.var.get(), self.init[0], 60, self.init[1], self.init[2])

    def run_loop(self, Screen):
        self.time = 0 if self.time >= 900 else self.time
        self.draw_motion(Screen) if self.data else self.draw_init_pend(Screen)
        self.time += 1 if self.play else 0

    def draw_motion(self, Screen):
        n_p = self.var.get()
        draw_coords = [convert_point(self.data[i][self.time], n_p) for i in range(n_p)]
        draw_coords.insert(0, convert_point([0, 0], n_p))
        draw_coords = np.array(draw_coords, dtype=int)

        [pg.draw.line(Screen, (254, 0, 0), draw_coords[i], draw_coords[i + 1], 8) for i in range(n_p)]
        [pg.draw.circle(Screen, (0, 0, 0), draw_coords[i], 4) for i in range(n_p + 1)]

    def rotate(self, mouse):
        n_p = self.var.get()
        ci = int(np.argmin([np.linalg.norm(np.array(mouse)-np.array(convert_point(x, n_p))) for x in self.init_coords]))

        vectors = [np.array(convert_point(self.init_coords[ci + cp + 1], n_p)) -
                   np.array(convert_point(self.init_coords[ci], n_p)) for cp in range(n_p-ci)]
        fulcrum = np.array(convert_point(self.init_coords[ci-1], n_p)) if ci != 0 \
            else np.array(convert_point([0, 0], n_p))
        length = np.linalg.norm(np.array(convert_point(self.init_coords[ci], n_p)) - fulcrum)
        vector = mouse-fulcrum
        self.init_coords[ci] = (length * vector/np.linalg.norm(vector) + fulcrum).tolist()
        for cp in range(n_p-ci):
            self.init_coords[ci+cp+1] = (np.array(self.init_coords[ci]) + vectors[cp]).tolist()

    def stretch(self, mouse):
        def inert_rod(length, mass):
            return (1 / 12) * mass * length ** 2

        n_p = self.var.get()
        ci = int(np.argmin([np.linalg.norm(np.array(mouse)-np.array(convert_point(x, n_p))) for x in self.init_coords]))
        if ci == 0:
            return
        vector = np.array(mouse) - np.array(convert_point(self.init_coords[ci], n_p))
        for cii in range(ci, n_p+1):
            self.init_coords[cii][0] += vector[0]
            self.init_coords[cii][1] += vector[1]

        normalizer = np.array([697, 694])/(n_p*6+2)
        new_vector = (np.array(mouse) - np.array(convert_point(self.init_coords[ci-1], n_p))) / normalizer
        new_length = np.linalg.norm(new_vector)

        self.init[0][(ci-1) * 4] = new_length
        self.init[0][(ci-1) * 4 + 1] = new_length/2
        self.init[0][(ci-1) * 4 + 2] = new_length * self.rod_density
        self.init[0][(ci-1) * 4 + 3] = inert_rod(new_length, new_length * self.rod_density)

    def init_pend(self):
        self.play, self.time, self.data = 0, 0, 0
        n_p = self.var.get()
        self.graph = draw_graph_pygame(np.array([]), np.array([]), (900, 900), n_p)

        def inert_rod(length, mass):
            return (1 / 12) * mass * length ** 2

        rod_length, rod_density = 3, 0.33
        rod = [rod_length, rod_length/2, self.rod_density*rod_length,
               inert_rod(rod_length, self.rod_density*rod_length)] * n_p
        rod.append(9.81)
        numerical_constants = np.array(rod)

        init_conditions = np.zeros(n_p * 2)
        init_conditions[0] = -np.pi

        input_torques = np.zeros(n_p)

        self.init = [numerical_constants, init_conditions, input_torques]
        self.init_coords = [[0, -int((i+1)*self.init[0][i*4])] for i in range(n_p)]
        self.init_coords.insert(0, [0, 0])

    def draw_init_pend(self, Screen):
        n_p = self.var.get()
        if self.init_coords:
            [pg.draw.line(Screen, (254, 0, 0), np.array(convert_point(self.init_coords[i], n_p), dtype=int),
                          np.array(convert_point(self.init_coords[i + 1], n_p), dtype=int), 8) for i in range(n_p)]
            [pg.draw.circle(Screen, (0, 0, 0), np.array(convert_point(self.init_coords[i], n_p), dtype=int), 4)
             for i in range(n_p + 1)]


def main():
    pg.init()
    width, height = (900, 900)
    Screen = pg.display.set_mode((width, height))
    pg.display.set_caption('pendulum')
    win = pag.getWindowsWithTitle('pendulum')
    win[0].moveTo(60, 60)
    clock = pg.time.Clock()

    root = tk.Tk()
    root.title('menu')
    control = Controller(master=root)

    rotate, stretch = 0, 0
    while True:
        Screen.blit(control.graph, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    rotate = 1
                elif event.button == 3:
                    stretch = 1
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    rotate = 0
                elif event.button == 3:
                    stretch = 0
        if rotate:
            control.rotate(pg.mouse.get_pos())
        if stretch:
            control.stretch(pg.mouse.get_pos())
        control.run_loop(Screen)

        try:
            control.update()
        except tk.TclError:
            sys.exit()
        pg.display.update()
        clock.tick(24)


if __name__ == '__main__':
    main()
