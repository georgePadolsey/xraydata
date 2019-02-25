import csv
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def linear_model(x,a,b):
    return x*a + b



with open('30kV.csv') as f:
    lines = csv.reader(f,delimiter='\t')
    xs = []
    ys = []
    header = True
    for line in lines:
        if header:
            header=False
            continue

        pline = list(map(lambda x: np.float64(x), line))
        xs.append(pline[0])
        ys.append(pline[1])


# find best lof



end_x = 10

res = []
cur_iter = 0
for cur_x_low in np.arange(2,end_x, 0.1):
    for cur_x_high in np.arange(cur_x_low,end_x, 0.1):

        v_xs = []
        v_ys = []

        for i in range(len(xs)):
            if cur_x_low < xs[i] < end_x:
                v_xs.append(xs[i])
                v_ys.append(ys[i])
        
        if len(v_xs) <= 5 or len(v_ys) <= 5:
            continue

        (grad, yint), pcov = curve_fit(linear_model, v_xs, v_ys)

        res.append([pcov[0,0], cur_x_low, cur_x_high])
        cur_iter += 1

s, min_x, max_x = min(res, key=lambda x: x[0])


v_xs = []
v_ys = []
min_x =3.6
max_x = 4.5
for i in range(len(xs)):
    if min_x < xs[i] < max_x:
        v_xs.append(xs[i])
        v_ys.append(ys[i])

(grad, yint), pcov = curve_fit(linear_model, v_xs, v_ys)

xint = -yint/grad

xint = xint/360 * 2* np.pi

d  =5.64e-10 /2
print(xint) 

def h_from_xint(xin):
    return ((2*d*np.sin(xint)) * (1.6e-19) * (30e3))/3e8
 

h = h_from_xint(xint)

print(h, h_from_xint(xint + pcov[0,0]**0.5) - h)
plt.plot(xs, ys)
plt.figure()
plt.plot(v_xs, v_ys)
plt.show()