import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
params= {'text.latex.preamble' : r'\usepackage{amsmath}'}
matplotlib.rcParams.update(params)
import matplotlib.pyplot as plt


# t = np.linspace(0.0, 1.0, 100)
# s = np.cos(4 * np.pi * t) + 2

fig, ax = plt.subplots(figsize=(4, 1.5), tight_layout=True)
# ax.plot(t, s)
fig.set_facecolor('#f0f0f0')
intro_text = r'Household solve the following dynamic optimization problem'
begin_align = r'\begin{align*}'
objective_function = r'\max_{C(t)}\int_{0}^{\infty}&\frac{C(t)^{1-\sigma}}{1-\sigma}e^{\rho t}dt \\'
constraint = r'\text{s.t. } \dot{a} &= w(t) L + r(t) a(t) - C(t) \\'
initial_condition = r'a(0) &= a_{0}'
end_align = r'\end{align*}'

fig.text(.02, .9, intro_text)
fig.text(.12, .55, begin_align + objective_function + constraint + initial_condition + end_align)
ax.set_facecolor('#f0f0f0')
ax.axis('off')
plt.savefig("C:/Users/htloe/Google Drive/HaTo/01_Arbeit/02_Weiterbildung/03_Python/Code/05-Projektarbeit/Relaxation/Pictures/households.png", bbox_inches='tight')
plt.show()