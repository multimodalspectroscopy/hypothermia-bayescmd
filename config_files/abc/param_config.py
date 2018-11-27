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


hypothermia_params = ['Dpsi_n',
                      'K_sigma',
                      'NADpool',
                      'Q_10',
                      'Xtot_n',
                      'cell_death',
                      'k_aut',
                      'pH_on',
                      'r_0']

prior_dict = {}
for p in hypothermia_params:
    prior_dict[p] = [param_df.loc[p, 'Dist. Type'], [
        param_df.loc[p, 'Min'], param_df.loc[p, 'Max']]]

# Set constant values
prior_dict['insult_nadir'] = ['constant', 0]
prior_dict['death_transition'] = ['constant', 0]


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
