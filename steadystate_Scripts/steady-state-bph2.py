""" Generate various steady state data sets."""
from bayescmd.steady_state import RunSteadyState
import os
import distutils
import json
import itertools
import copy
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib import rcParams
import numpy as np

MODEL_NAME = "bp_hypothermia_2"

# inputs = {"P_a": (30, 70), "Pa_CO2": (8, 160), "SaO2sup": (0.2, 1.0)}

# temperatures = [37, 35, 33.5]

# cbar = sns.color_palette("muted", n_colors=4)

# for direction in ["up", "down"]:
#     for i, r in inputs.items():
#         data = {}
#         workdir = os.path.join(
#             os.pardir, 'data', 'steady_state', MODEL_NAME, "autoregulation")
#         distutils.dir_util.mkpath(workdir)
#         distutils.dir_util.mkpath(os.path.join(workdir, "Figures"))
#         print("Running steady state - {}".format(i))
#         for t in temperatures:
#             print("Running temperature {}C".format(t))
#             config = {
#                 "model_name": MODEL_NAME,
#                 "inputs": i,
#                 "parameters": {
#                     "temp": t
#                 },
#                 "targets": ["CBF"],
#                 "max_val": r[1],
#                 "min_val": r[0],
#                 "debug": True,
#                 "direction": direction
#             }

#             model = RunSteadyState(conf=config, workdir=workdir)
#             output = model.run_steady_state()
#             data[t] = output
#             with open(os.path.join(workdir,
#                                    "{}_{}.json".format(i, direction)), 'w') as f:
#                 json.dump(data, f)

#         fig, ax = plt.subplots()
#         for idx, t in enumerate(temperatures):
#             ax.plot(data[t][i], data[t]['CBF'], label=t, color=cbar[idx])

#         ax.set_title("Steady state for varying {} - {}".format(i, direction))
#         ax.set_ylabel("CBF")
#         ax.set_xlabel(i)
#         legend = ax.legend(loc='upper center')

#         fig.savefig(os.path.join(workdir, "Figures", "{}_{}.png".format(i, direction)),
#                     bbox_inches="tight")


# For debugging
# outputs.extend(["k_MAshut", "k_nMAshut", "Q_temp", "_ADP", "_ATP"])

q10_met_range = np.arange(0.1, 5.1, 0.1)
q10_haemo_range = np.arange(0.1, 5.1, 0.1)
q_range = list(itertools.product(q10_met_range, q10_haemo_range))
pa_range = [30, 40, 50, 60, 70]
sao2_range = [0.8, 0.9, 1.0]

outputs = ["CMRO2", "CCO", "HbT", "CBF", "Hbdiff",
           "TOI", "Vmca", "HbO2", "HHb"]

cbar = sns.color_palette("Set1", n_colors=len(q10_met_range))

data = {}
direction = "down"
workdir = os.path.join(os.pardir, 'data', 'steady_state', MODEL_NAME,
                       "model_output")
distutils.dir_util.mkpath(workdir)

for q in q_range:
    print("Running Q10_met {}, Q10_haemo {}".format(q[0], q[1]))

    config = {
        "model_name": MODEL_NAME,
        "inputs": "temp",
        "parameters": {
            "Q_10_met": q[0],
            "Q_10_haemo": q[1]
        },
        "targets": copy.copy(outputs),
        "max_val": 37,
        "min_val": 33.5,
        "debug": False,
        "direction": direction
    }

    model = RunSteadyState(conf=config, workdir=workdir)
    output = model.run_steady_state()
    data["{}_{}".format(q[0], q[1])] = output

with open(os.path.join(workdir, "q_range_runs_{}.json".format(direction)), 'w') as f:
    json.dump(data, f)
# rcParams['axes.titlepad'] = 12

# for o in outputs:
#     print("Plotting {}".format(o))
#     if direction == "both":
#         fig, ax = plt.subplots(nrows=len(q10_met_range),
#                                ncols=len(q10_haemo_range), figsize=(10, 10), sharey=True)
#         for idx, q in enumerate(q_range):
#             q_key = "{}_{}".format(q[0], q[1])
#             ax[idx//len(q10_met_range)][idx % len(q10_haemo_range)].plot(data[q_key]["temp"][:len(data[q_key][o]) // 2 + 1],
#                                                                          data[q_key][o][:len(
#                                                                              data[q_key][o]) // 2 + 1],
#                                                                          label="Up")
#             ax[idx//len(q10_met_range)][idx % len(q10_haemo_range)].plot(data[q_key]["temp"][len(data[q_key][o]) // 2:],
#                                                                          data[q_key][o][len(
#                                                                              data[q_key][o]) // 2:],
#                                                                          label="Down")

#             ax[idx//len(q10_met_range)][idx %
#                                         len(q10_haemo_range)].set_title("Q10_met: {} Q10_haemo: {}".format(q[0], q[1]))
#             ax[idx//len(q10_met_range)][idx %
#                                         len(q10_haemo_range)].set_ylabel(o)
#             ax[idx//len(q10_met_range)][idx %
#                                         len(q10_haemo_range)].set_xlabel("Temp (C)")
#         # ax[idx//5][idx % 5].legend()
#         plt.tight_layout()
#         plt.subplots_adjust(hspace=0.4)
#         path = os.path.join(workdir, "Figures")
#         distutils.dir_util.mkpath(path)
#         fig.savefig(os.path.join(path, "{}_both.png".format(o)),
#                     bbox_inches="tight")
#         plt.close()

#     else:
#         fig, ax = plt.subplots(nrows=len(q10_met_range),
#                                ncols=len(q10_haemo_range), figsize=(10, 10), sharey=True)
#         for idx, q in enumerate(q_range):
#             q_key = "{}_{}".format(q[0], q[1])
#             ax.flatten()[idx].plot(data[q_key]["temp"],
#                                    data[q_key][o], label="$Q_{10,met}$: %f\n$Q_{10,haemo}$: %f" % (q[0], q[1]))
#             ax.flatten()[idx].set_title(
#                 "%s response to Temperature for different\n$Q_{10,met}$ and $Q_{10,haemo}$ values - %s" % (o, direction))
#             ax.flatten()[idx].set_ylabel(o)
#             ax.flatten()[idx].set_xlabel("Temp (C)")
#         # ax.flatten()[idx].legend()

#         path = os.path.join(workdir, "Figures")

#         distutils.dir_util.mkpath(path)
#         fig.savefig(os.path.join(path, "{}_{}.png".format(o, direction)),
#                     bbox_inches="tight")
#         plt.close()
