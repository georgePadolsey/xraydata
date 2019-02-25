import csv
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import glob
import os

manual_cuts = {
    26: [4.5, 5],
    30: [4.2, 4.8],
    34: [3.5, 4.2],

    35: [3.4, 3.9]
}


def linear_model(x, a, b):
    return x*a + b


d = 5.64e-10 / 2

all_data = []
for cFile in glob.glob("*.csv"):
    data = {
        "voltage": float(cFile.split(".")[0][:-2]),
        "xs": [],
        "ys": []
    }
    with open(cFile) as f:
        lines = csv.reader(f, delimiter='\t')

        header = True
        for line in lines:
            if header:
                header = False
                continue

            line = [line[0], line[1]]

            pline = list(map(lambda x: np.float64(x), line))
            data["xs"].append(pline[0])
            data["ys"].append(pline[1])

    all_data.append(data)
    plt.figure()
    plt.title(data["voltage"])
    plt.plot(data["xs"], data["ys"])
# plt.show()


n_xs = []
n_ys = []
for data in all_data:
    if data["voltage"] not in manual_cuts:
        continue

    min_x, max_x = manual_cuts[data["voltage"]]
    xs = data["xs"]
    ys = data["ys"]
    v_xs = []

    v_ys = []
    for i in range(len(xs)):
        if min_x < xs[i] < max_x:
            v_xs.append(xs[i])
            v_ys.append(ys[i])

    (grad, yint), pcov = curve_fit(linear_model, v_xs, v_ys)
    xint = -yint/grad

    xint = xint/360 * 2 * np.pi
    min_lam = 2 * d * np.sin(xint)
    n_xs.append(1/data["voltage"])
    n_ys.append(min_lam)


plt.figure()
plt.scatter(n_xs, n_ys)


(grad, yint), pcov = curve_fit(linear_model, n_xs, n_ys)

print(grad/(3e8/(1.6e-19)))

plt.show()
