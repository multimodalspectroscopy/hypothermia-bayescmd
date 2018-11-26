from bayescmd.abc import priors_creator
"""Create BayesCMD configuration file for PLOS simulated data."""
import pandas as pd
import json
from pathlib import Path
import os.path as op
p = Path(op.abspath(__file__))

current_file = Path(op.abspath(__file__))

param_df = pd.read_csv(op.join(current_file.parents[2],
                               'bcmd-files',
                               'sensitivity',
                               'param_files',
                               'bp_hypothermia_params.csv'
                               ),
                       header=None,
                       names=['Parameter', 'Dist. Type',
                              'Min', 'Max', 'Default'],
                       index_col=0)


hypothermia_params = ['NADpool', 'k_aut', 'P_an', 'P_ic', 'a_frac_n', 'Xtot_n',
                      'r_0', 'r_t', 'CMRO2_n', 'pH_on', 'temp_n', 'Q_10', 'phi', 'r_m', 'Dpsi_n', 'r_n']

prior_dict = {}
for p in hypothermia_params:
    prior_dict[p] = [param_df.loc[p, 'Dist. Type'], [
        param_df.loc[p, 'Min'], param_df.loc[p, 'Max']]]


config_dict = {"model_name": "bp_hypothermia",
               "inputs": ["SaO2sup", "P_a", "temp"],
               "create_params": False,
               "priors": prior_dict,
               "targets": ["CCO", "HbT", "Hbdiff", "HbO2", "HHb"],
               "zero_flag": {
                   "CCO": True,
                   "Hbdiff": True,
                   "HbT": True,
                   "HbO2": True,
                   "HHb": True
               },
               "batch_debug": False,
               "store_simulations": False
               }

with open(op.join('.', 'bp_hypothermia_config.json'
                  ),
          'w') as f:
    json.dump(config_dict, f)
