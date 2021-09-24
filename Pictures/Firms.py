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
intro_text = r'The firm maximizes profits in a perfectly competitive environment'
begin_align = r'\begin{align*}'
profit_function = r'\Pi (K(t), L) = K(t)^{\alpha} (A L)^{1-\alpha} - w(t) L - (r(t) + \delta) K(t)'
end_align = r'\end{align*}'
maximization_text = r'This implies that the firm hires labor and rents capital such that'
interest_rate = r' r(t) &= K(t)^{\alpha-1} (A L)^{1-\alpha} - \delta\\'
wage_rate = r'w(t) &= (1-\alpha) K(t)^{\alpha} (A L)^{-\alpha}'

fig.text(.02, .9, intro_text)
fig.text(.12, .7, begin_align + profit_function + end_align)
fig.text(.02, .5, maximization_text)
fig.text(.12, .3, begin_align + interest_rate + wage_rate + end_align)

ax.set_facecolor('#f0f0f0')
ax.axis('off')
plt.savefig("C:/Users/htloe/Google Drive/HaTo/01_Arbeit/02_Weiterbildung/03_Python/Code/05-Projektarbeit/Relaxation/Pictures/firms.png", bbox_inches='tight')
plt.show()