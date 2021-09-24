# Packages for numerical calculations
import numpy as np
from scipy.optimize import root
# Packages for plotting
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# Packages for GUI
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
# Ensure that the right backend is used
matplotlib.use("TkAgg")



class Ramsey:
    """ A Class to solve the Ramsey model using the Relaxation Alogrithm.
        This can be used as a proto-type to solve any differential-algebraic system.
    """
    def __init__(self, masterframe):
        # For use in functions
        self.masterframe = masterframe
        # masterframe.grid()

        # Initial values for parameters
        self.tk_rho = tk.StringVar(masterframe, ".02")
        self.tk_sigma = tk.StringVar(masterframe, "1.")
        self.tk_alpha = tk.StringVar(masterframe, ".35")
        self.tk_delta = tk.StringVar(masterframe, ".08")
        self.tk_A = tk.StringVar(masterframe, "1.")
        self.tk_L = tk.StringVar(masterframe, "1.")
        self.tk_n = tk.StringVar(masterframe, "101")
        self.tk_K_i = tk.StringVar(masterframe, "6")

        # Initial values for steady state, given initial values for parameters as defined above
        self.K_steady = tk.StringVar()
        self.C_steady = tk.StringVar()
        self.r_steady = tk.StringVar()
        self.w_steady = tk.StringVar()
        self.update_steady_values("")  # Show steady state value upon inception

        # Generate an additional Frame for text
        textframe = ttk.Frame(master=masterframe)
        textframe.grid(row=1, column=1, sticky="n")
        # Generate additional LabelFrames to
        labelframe_parameters = ttk.LabelFrame(textframe, text="Parameters of the Ramsey model")
        labelframe_variables = ttk.LabelFrame(textframe, text="Steady state level of")
        labelframe_description = ttk.LabelFrame(textframe, text="General description of the Ramsey Model")

        labelframe_parameters.grid(row=0, column=0, sticky="nsew")
        labelframe_variables.grid(row=1, column=0, sticky="nsew")
        labelframe_description.grid(row=2, column=0, sticky="nsew")

        # Collection of all parameters of the model
        parameters = [["\u03C1", self.tk_rho],
                      ["\u03C3", self.tk_sigma],
                      ["\u03B1", self.tk_alpha],
                      ["\u03B4", self.tk_delta],
                      ["A", self.tk_A],
                      ["L", self.tk_L],
                      ["n", self.tk_n],
                      ["K₀", self.tk_K_i]]

        # Labels and entry fields for all parameters of the model
        for i, parameter in enumerate(parameters):
            ttk.Label(labelframe_parameters, text=parameter[0]).grid(row=i, column=0, sticky="e")
            ttk.Entry(labelframe_parameters, textvariable=parameter[1]).grid(row=i, column=1)

        # Collection of all variables of the model in steady state
        variables = [["Capital", self.K_steady],
                     ["Consumption", self.C_steady],
                     ["Interest rate", self.r_steady],
                     ["Wage rate", self.w_steady]]

        # Labels for the steady state values of the dynamic system's variables
        for i, variable in enumerate(variables):
            ttk.Label(labelframe_variables, text=f"{variable[0]}:").grid(row=i, column=0, sticky="e")
            ttk.Label(labelframe_variables, textvariable=variable[1]).grid(row=i, column=1, sticky="e")

        # Dynamically update steady state values
        textframe.bind_all("<Leave>", self.update_steady_values)

        # Generate the plot of the transition
        self.BgColorTkinter = "#f0f0f0"
        self.fig, self.ax = plt.subplots(2, 2, dpi=100, figsize=(10, 6))
        self.fig.set_facecolor(self.BgColorTkinter)

        # Generate Canvas for plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=masterframe)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        # Plot transition upon inception
        self.ramsey_plot()

        # Generate toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, masterframe, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=0, column=0)

        # Dynamically update transition
        textframe.bind_all("<Button-1>", self.ramsey_plot)

        # Add description for the economic model
        nb = ttk.Notebook(labelframe_description)
        tab1 = ttk.Frame(nb)
        tab2 = ttk.Frame(nb)
        tab3 = ttk.Frame(nb)
        nb.add(tab1, text="Households")
        nb.add(tab2, text="Firms")
        nb.add(tab3, text="Dynamic System")
        nb.grid()

        self.image_households = PhotoImage(file="Pictures/households.png")
        self.image_firms = PhotoImage(file="Pictures/firms.png")
        self.image_dynamic_system = PhotoImage(file="Pictures/dynamic_system.png")

        label_tab1 = tk.Label(tab1)
        label_tab2 = tk.Label(tab2)
        label_tab3 = tk.Label(tab3)

        label_tab1['image'] = self.image_households
        label_tab2['image'] = self.image_firms
        label_tab3['image'] = self.image_dynamic_system

        label_tab1.grid(sticky="nsew")
        label_tab2.grid(sticky="nsew")
        label_tab3.grid(sticky="nsew")

        # Exit button
        button = ttk.Button(textframe, text="Quit", command=self.masterframe.quit)
        button.grid(row=14, column=0, columnspan=2, sticky="sew")

        # Set the position of the master-Frame
        x = (masterframe.winfo_screenwidth() - masterframe.winfo_reqwidth()) / 2
        y = (masterframe.winfo_screenheight() - masterframe.winfo_reqheight()) / 2
        masterframe.geometry("+%d+%d" % (x - 500, y - 250))

        # Rename Window
        masterframe.title("Solution to the Ramsey Model using the Relaxation Algorithm")

        # Change appearance
        style = ttk.Style(masterframe)
        style.theme_use("xpnative")

    def update_parameters(self):
        """ A method to update the parameters for further use in update_steady_state() and ramsey_plot(). """
        self.n = int(self.tk_n.get())

        self.rho = float(self.tk_rho.get())
        self.sigma = float(self.tk_sigma.get())
        self.alpha = float(self.tk_alpha.get())
        self.delta = float(self.tk_delta.get())
        self.A = float(self.tk_A.get())
        self.L = float(self.tk_L.get())

        self.K_i = float(self.tk_K_i.get())

    def update_steady_values(self, event):
        """ A method to update the displayed steady state to the Ramsey model. """
        self.update_parameters()
        sol_steady = self.steady_state()
        self.K_steady.set(round(sol_steady.x[0], 2))
        self.C_steady.set(round(sol_steady.x[1], 2))
        self.r_steady.set(round(sol_steady.x[2], 2))
        self.w_steady.set(round(sol_steady.x[3], 2))

    def ramsey_plot(self, event=None):
        """ A method to plot the resulting the transitional dynamics of the Ramsey model. """
        self.update_parameters()
        sol_t = self.transition(self.K_i)
        sol_s = self.steady_state()
        titles = ["Capital", "Consumption", "Interest rate", "Wage rate"]

        k = 0
        for i in range(2):
            for j in range(2):
                self.ax[i, j].cla()
                self.ax[i, j].set_facecolor(self.BgColorTkinter)
                self.ax[i, j].set_xlabel("years")
                self.ax[i, j].plot(sol_t.x[k * self.n + 1: (k + 1) * self.n])
                self.ax[i, j].axhline(sol_s.x[k], c="r", linestyle="dashed")
                self.ax[i, j].set_xlim([0, self.n])
                self.ax[i, j].set_title(titles[k])
                k += 1
        plt.tight_layout()
        self.canvas.draw()

    def steady_state(self):
        """ A method to calculate the steady state of the Ramsey model. """
        def fun(x):
            K, C, r, w = x
            f = [r * K + w * self.L - C,
                 1 / self.sigma * (r - self.rho),
                 r - (self.alpha * K ** (self.alpha - 1) * (self.A * self.L) ** (1 - self.alpha) - self.delta),
                 w - (1 - self.alpha) * K ** self.alpha * (self.A * self.L) ** (- self.alpha)
                ]
            return f
        sol_s = root(fun, np.array([1, 1, 1, 1]))
        return sol_s

    def start_values(self):
        """ A method to generate an initial guess to calculate the transitional dynamics of the Ramsey model. """
        steady_state_values = self.steady_state().x
        s_v = []
        for value in steady_state_values:
            guess = [value for i in range(self.n)]
            s_v = s_v + guess
        s_v = np.array(s_v)
        return s_v

    def transition(self, K_initial):
        """ A method to calculate the transitional dynamics of the Ramsey model. """
        def fun(x):
            f = []
            aux = []
            for j in range(self.n):
                [K, C, r, w] = [x[j - 1], x[self.n + j], x[2 * self.n + j], x[3 * self.n + j]]
                K1 = x[j]
                C1 = x[self.n + j + 1]
                system = [K1 - K - (r * K + w * self.L - C),
                          C1 - C - C / self.sigma * (r - self.rho),
                          r - (self.alpha * K ** (self.alpha - 1) * (self.A * self.L) ** (1 - self.alpha) - self.delta),
                          w - (1 - self.alpha) * K ** self.alpha * (self.A * self.L) ** (- self.alpha)
                          ]
                aux.append(system)
            aux = [[aux[z][y] for z in range(len(aux))] for y in range(len(aux[0]))]
            for i in aux:
                f = f + i
            f[0] = x[0] - K_initial
            f[2 * self.n] = x[2 * self.n] - self.steady_state().x[1]
            return f
        sol_t = root(fun, self.start_values())
        return sol_t


if __name__ == '__main__':
    master = tk.Tk()
    Ramsey_object = Ramsey(master)
    master.mainloop()
