""" Generate various steady state data sets."""
from bayescmd.steady_state import RunSteadyState
import os
import distutils
import json
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

MODEL_NAME = "bp_hypothermia_2"

inputs = {"P_a": (30, 70), "Pa_CO2": (8, 160), "SaO2sup": (0.2, 1.0)}

temperatures = [37, 35, 33.5]

cbar = sns.color_palette("muted", n_colors=4)

for direction in ["up", "down"]:
    for i, r in inputs.items():
        data = {}
        workdir = os.path.join(os.pardir, 'data', 'steady_state', MODEL_NAME)
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

        fig.savefig(os.path.join(workdir, "Figures", "{}_{}.png".format(i, direction),
                    bbox_inches="tight"))

outputs = ["CMRO2", "CCO", "DHbT", "CBF", "DHbdiff", "TOI", "Vmca", "DHbO2", "DHHb", "HHb", "HbO2"]


# For debugging
# outputs.extend(["k_MAshut", "k_nMAshut", "Q_temp", "_ADP", "_ATP"])

q10_met_range = [1, 1.5, 2, 2.5, 3, 3.5]
q10_haemo_range = [1, 1.5, 2, 2.5, 3, 3.5]
q_range = itertools.product(q10_met_range, q10_haemo_range)
pa_range = [30, 40, 50, 60, 70]
sao2_range = [0.8, 0.9, 1.0]
cbar = sns.color_palette("Set1", n_colors=len(pa_range))

data = {}
direction = "both"
workdir = os.path.join(os.pardir, 'data,' 'steady_state', MODEL_NAME,
                       "model_parameters")
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
        "targets": outputs,
        "max_val": 37,
        "min_val": 33.5,
        "debug": False,
        "direction": direction
    }

    model = RunSteadyState(conf=config, workdir=workdir)
    output = model.run_steady_state()
    data[q] = output

with open(os.path.join(workdir, "q_range_runs.json"), 'w') as f:
    json.dump(data, f)

for o in outputs:
    if direction == "both":
        fig, ax = plt.subplots(nrows=1, ncols=len(q_range))
        for idx, q in enumerate(q_range):
            ax[idx].plot(data[q]["temp"][:len(data[q][o]) // 2 + 1],
                         data[q][o][:len(data[q][o]) // 2 + 1],
                         label="Up")
            ax[idx].plot(data[q]["temp"][len(data[q][o]) // 2:],
                         data[q][o][len(data[q][o]) // 2:],
                         label="Down")

            ax[idx].set_title("Q10_met: {} Q10_haemo: {}".format(q[0], q[1]))
            ax[idx].set_ylabel(o)
            ax[idx].set_xlabel("Temp (C)")
        ax[idx].legend()
        plt.tight_layout()

        path = os.path.join(workdir, "Figures", "varying_q10")
        distutils.dir_util.mkpath(path)
        fig.savefig(os.path.join(path, "{}_both.png".format(o)),
                    bbox_inches="tight")
        plt.close()

    else:
        fig, ax = plt.subplots()
        for idx, q in enumerate(q_range):
            ax.plot(data[q]["temp"],
                    data[q][o], label=q, color=cbar[idx])
        ax.set_title(
            "{} response to Temperature for different\nQ10_met and Q10_haemo values - {}".format(o, direction))
        ax.set_ylabel(o)
        ax.set_xlabel("Temp (C)")
        ax.legend()

        path = os.path.join(workdir, "Figures", "varying_q10")

        distutils.dir_util.mkpath(path)
        fig.savefig(os.path.join(path, "{}_{}.png".format(o, direction)),
                    bbox_inches="tight")
        plt.close()