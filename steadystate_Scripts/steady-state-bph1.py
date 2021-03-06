""" Generate various steady state data sets."""
from bayescmd.steady_state import RunSteadyState
import numpy as np
import os
import distutils
import json
import itertools
import copy
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib import rcParams

MODEL_NAME = "bp_hypothermia_1"

inputs = {"P_a": (30, 70), "Pa_CO2": (8, 160), "SaO2sup": (0.2, 1.0)}

temperatures = [37, 35, 33.5]

cbar = sns.color_palette("muted", n_colors=4)

for direction in ["up", "down"]:
    for i, r in inputs.items():
        data = {}
        workdir = os.path.join(
            os.pardir, 'data', 'steady_state', MODEL_NAME, "autoregulation")
        distutils.dir_util.mkpath(workdir)
        distutils.dir_util.mkpath(os.path.join(workdir, "Figures"))
        print("Running steady state - {}".format(i))
        for t in temperatures:
            print("Running temperature {}C".format(t))
            config = {
                "model_name": MODEL_NAME,
                "inputs": i,
                "parameters": {
                    "temp": t
                },
                "targets": ["CBF"],
                "max_val": r[1],
                "min_val": r[0],
                "debug": True,
                "direction": direction
            }

            model = RunSteadyState(conf=config, workdir=workdir)
            output = model.run_steady_state()
            data[t] = output
            with open(os.path.join(workdir,
                                   "{}_{}.json".format(i, direction)), 'w') as f:
                json.dump(data, f)

        fig, ax = plt.subplots()
        for idx, t in enumerate(temperatures):
            ax.plot(data[t][i], data[t]['CBF'], label=t, color=cbar[idx])

        ax.set_title("Steady state for varying {} - {}".format(i, direction))
        ax.set_ylabel("CBF")
        ax.set_xlabel(i)
        legend = ax.legend(loc='upper center')

        fig.savefig(os.path.join(workdir, "Figures", "{}_{}.png".format(i, direction)),
                    bbox_inches="tight")


# For debugging
# outputs.extend(["k_MAshut", "k_nMAshut", "Q_temp", "_ADP", "_ATP"])

q10_range = np.arange(0.1, 5.1, 0.1)
pa_range = [30, 40, 50, 60, 70]
sao2_range = [0.8, 0.9, 1.0]

outputs = ["CMRO2", "CCO", "HbT", "CBF", "Hbdiff",
           "TOI", "Vmca", "HbO2", "HHb"]

cbar = sns.color_palette("Set1", n_colors=len(q10_range))

data = {}
direction = "down"
workdir = os.path.join(os.pardir, 'data', 'steady_state', MODEL_NAME,
                       "model_output")
distutils.dir_util.mkpath(workdir)

for q in q10_range:
    print("Running Q10 {}".format(q))

    config = {
        "model_name": MODEL_NAME,
        "inputs": "temp",
        "parameters": {
            "Q_10": q,
        },
        "targets": copy.copy(outputs),
        "max_val": 37,
        "min_val": 33.5,
        "debug": False,
        "direction": direction
    }

    model = RunSteadyState(conf=config, workdir=workdir)
    output = model.run_steady_state()
    data[q] = output

with open(os.path.join(workdir, "q_range_runs_{}.json".format(direction)), 'w') as f:
    json.dump(data, f)
# rcParams['axes.titlepad'] = 12

# for o in outputs:
#     if direction == "both":
#         fig, ax = plt.subplots(nrows=1, ncols=len(
#             q10_range), sharey=True, figsize=(9, 4))
#         for idx, q in enumerate(q10_range):
#             ax[idx].plot(data[q]["temp"][:len(data[q][o]) // 2 + 1],
#                          data[q][o][:len(data[q][o]) // 2 + 1],
#                          label="Warming")
#             ax[idx].plot(data[q]["temp"][len(data[q][o]) // 2:],
#                          data[q][o][len(data[q][o]) // 2:],
#                          label="Cooling")

#             ax[idx].set_title("$Q_{10}$: %s"%(q))
#             ax[idx].set_ylabel(o)
#             ax[idx].set_xlabel("Temp ($^{\circ}$C)")
#         ax[idx].legend()
#         plt.tight_layout()

#         path = os.path.join(workdir, "Figures")

#         distutils.dir_util.mkpath(path)
#         fig.savefig(os.path.join(path, "{}_both.png".format(o)),
#                     bbox_inches="tight")
#         plt.close()

#     else:
#         fig, ax = plt.subplots(ncols=1, nrows=len(
#             q10_range), sharey=True, figsize=(5, 10))
#         for idx, q in enumerate(q10_range):
#             # if direction == "both":
#             #     ax.plot(output["temp"][:len(output[o]) // 2 + 1],
#             #             output[o][:len(output[o]) // 2 + 1],
#             #             label="Up")
#             #     ax.plot(output["temp"][len(output[o]) // 2:],
#             #             output[o][len(output[o]) // 2:],
#             #             label="Down")
#             # else:
#             ax[idx].plot(data[q]["temp"],
#                          data[q][o], label=q, color=cbar[idx])
#         ax[idx].set_title(
#             "{} response to Temperature for different Q10 values".format(o))
#         ax[idx].set_ylabel(o)
#         ax[idx].set_xlabel("Temp (C)")
#         ax[idx].legend()

#         path = os.path.join(workdir, "Figures")

#         distutils.dir_util.mkpath(path)
#         fig.savefig(os.path.join(path, "{}.png".format(o)),
#                     bbox_inches="tight")
#         plt.close()
