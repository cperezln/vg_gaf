from ts2vg import HorizontalVG
import numpy as np


time_points = np.linspace(0, 4 * np.pi, 1000)
x = np.sin(time_points)
X = np.array([x])
vg = HorizontalVG()
vg.build(X)

vg.summary
