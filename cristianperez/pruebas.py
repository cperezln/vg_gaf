from gadf import gadf
from gasf import gasf
from vg import vg
from hvg import hvg
from network_utils import white_noise, plot_hist
from random import gauss
import pandas
from pandas import Series
import numpy as np
from collections import Counter
import math
import matplotlib.pyplot as plt

def vgadf(m):
    ln = len(m)
    rm = [[0]*ln for _ in range(ln)]
    for i in range(ln):
        h = -2
        for j in range(i + 1, ln):
            if i == 2 and j == 4:
                print("oh shit here we go again")
            if m[i][j] > 0:
                rm[i][j] = 1
                rm[j][i] = 1
                break
            elif m[i][j] < 0 and m[i][j] > h:
                rm[i][j] = 1
                rm[j][i] = 1
                h = m[i][j]
            elif m[i][j] == 0:
                rm[i][j] = i + 1 == j
                rm[j][i] = i + 1 == j
            elif m[i][j] < 0:
                pass
    return rm

time_series = np.abs(white_noise(7))
time_series = [0.6261980632740096, 1.1325347805326114, 1.8952910287771279, 0.054125543484939996, 1.1000466854422157, 0.4884443565563428, 0.46420856816351436, 0.8853393280710156, 0.7531830979554146, 0.547791314118154]
gramian = gadf(time_series)
tgadf = vgadf(gramian)

print(tgadf)