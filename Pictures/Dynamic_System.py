import matplotlib
matplotlib.rcParams['text.usetex'] = True
params = {'text.latex.preamble' : r'\usepackage{amsmath}'}
matplotlib.rcParams.update(params)
import matplotlib.pyplot as plt


# t = np.linspace(0.0, 1.0, 100)
# s = np.cos(4 * np.pi * t) + 2

fig, ax = plt.subplots(figsize=(4, 1.5), tight_layout=True)
# ax.plot(t, s)
fig.set_facecolor('#f0f0f0')
intro_text = r'The complete dynamic system is given by'
begin_align = r'\begin{align*}'
keynes_ramsey_rule = r'\frac{\dot{C}}{C(t)} &= \frac{1}{\sigma}(r-\rho)\\'
constraint = r'\dot{K} &= w(t) L + r(t) K(t) - C(t) \\'
interest_rate = r' r(t) &= K(t)^{\alpha-1} (A L)^{1-\alpha} - \delta\\'
wage_rate = r'w(t) &= (1-\alpha) K(t)^{\alpha} (A L)^{-\alpha}'
end_align = r'\end{align*}'

fig.text(.02, .9, intro_text)
fig.text(.12, .55, begin_align + keynes_ramsey_rule + constraint + interest_rate + wage_rate + end_align)
ax.set_facecolor('#f0f0f0')
ax.axis('off')
plt.savefig("C:/Users/htloe/Google Drive/HaTo/01_Arbeit/02_Weiterbildung/03_Python/Code/05-Projektarbeit/Relaxation/Pictures/dynamic_system.png", bbox_inches='tight')
plt.show()