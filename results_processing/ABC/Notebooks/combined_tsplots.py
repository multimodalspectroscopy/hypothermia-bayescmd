#!/usr/bin/env python
# coding: utf-8

# # Processing results using BigQuery #
#
# We start by importing all the requisite packages from BayesCMD etc. as well as ones required to plot and read data from big query.

# In[1]:


import string
import time
import os
import argparse
from pathlib import Path
import json
import matplotlib.pyplot as plt
import seaborn as sns
from distutils import dir_util
from pprint import pprint
import pickle
import pandas as pd
import random
import pprint
import numpy as np
import datetime

# BayesCMD packages
from bayescmd.results_handling import kde_plot
from bayescmd.results_handling import scatter_dist_plot
from bayescmd.results_handling import data_import
from bayescmd.results_handling import plot_repeated_outputs
from bayescmd.results_handling import histogram_plot
from bayescmd.results_handling import data_merge_by_batch
from bayescmd.abc import import_actual_data
from bayescmd.abc import priors_creator
from bayescmd.abc import get_distance
from bayescmd.abc import inputParse
from bayescmd.bcmdModel import ModelBCMD
from subprocess import TimeoutExpired, CalledProcessError  # noqa

# Google BigQuery
from google.cloud import bigquery
get_ipython().run_line_magic('load_ext', 'google.cloud.bigquery')


# In[2]:


# Explicitly use service account credentials by specifying the private
# key file. All clients in google-cloud-python have this helper.
client = bigquery.Client.from_service_account_json(
    "../../gcloud/hypothermia-auth.json"
)


# In[3]:


def generate_histogram_query(project, dataset, model, n_bins, distance):
    histogram_query = """
    SELECT
      MIN(data.{distance}) AS min,
      MAX(data.{distance}) AS max,
      COUNT(data.{distance}) AS num,
      INTEGER((data.{distance}-value.min)/(value.max-value.min)*{n_bins}) AS group_
    FROM
      [{project}:{dataset}.{model}] data
    CROSS JOIN (
      SELECT
        MAX({distance}) AS max,
        MIN({distance}) AS min
      FROM
        [{project}:{dataset}.{model}]) value
    GROUP BY
      group_
    ORDER BY
      group_
    """.format(dataset=dataset, model=model, n_bins=n_bins, distance=distance, project=project)
    return histogram_query


# In[4]:


def generate_posterior_query(project, dataset, model, distance, parameters, limit=50000):
    unpacked_params = ",\n".join(parameters)
    histogram_query = """
SELECT
    {unpacked_params},
    {distance},
    idx
FROM
  `{project}.{dataset}.{model}`
ORDER BY
  {distance} ASC
LIMIT
  {limit}
    """.format(project=project, dataset=dataset, model=model, unpacked_params=unpacked_params, distance=distance, limit=limit)
    return histogram_query


# In[5]:


def load_configuration(model_version, dataset, verbose=False):
    current_file = Path(os.path.abspath(''))
    config_file = os.path.join(current_file.parents[2],
                               'config_files',
                               'abc',
                               'bp_hypothermia_{}'.format(model_version),
                               'bp_hypothermia_{}_config.json'.format(
                                   model_version)
                               )

    with open(config_file, 'r') as conf_f:
        conf = json.load(conf_f)

    params = conf['priors']

    input_path = os.path.join(current_file.parents[2],
                              'data',
                              'clean_hypothermia',
                              '{}_filtered_formatted.csv'.format(dataset.upper()))

    d0 = import_actual_data(input_path)

    targets = conf['targets']
    model_name = conf['model_name']
    inputs = conf['inputs']

    config = {
        "model_name": model_name,
        "targets": targets,
        "inputs": inputs,
        "parameters": params,
        "input_path": input_path,
        "zero_flag": conf['zero_flag'],
    }

    if verbose:
        pprint(config)

    return config, d0


# In[6]:


configuration = {}

combinations = [('0', 'LWP475'), ('0', 'LWP479'),
                ('1', 'LWP475'), ('1_1', 'LWP479'),
                ('2', 'LWP475'), ('2_1', 'LWP479'),
                ('4', 'LWP475'), ('4_1', 'LWP479')]


for combo in combinations:

    model_number = combo[0]
    DATASET = combo[1]

    model_name = 'bph{}'.format(model_number)
    if model_name not in configuration.keys():
        configuration[model_name] = {}

    configuration[model_name][DATASET] = {}

    config, d0 = load_configuration(model_number, DATASET)
    configuration[model_name][DATASET]['bayescmd_config'] = config
    configuration[model_name][DATASET]['original_data'] = d0

    configuration[model_name][DATASET]['histogram_query'] = generate_histogram_query('hypothermia-bayescmd',
                                                                                     DATASET,
                                                                                     model_name,
                                                                                     100,
                                                                                     'NRMSE')

    configuration[model_name][DATASET]['posterior_query'] = generate_posterior_query('hypothermia-bayescmd',
                                                                                     DATASET,
                                                                                     model_name,
                                                                                     'NRMSE',
                                                                                     list(configuration[model_name][DATASET]['bayescmd_config']['parameters'].keys()))


# In[7]:


configuration['bph0'].keys()


# In[8]:


class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name,)
        print('Elapsed: %s' % (time.time() - self.tstart))


# In[9]:


def run_model(model):
    """Run a BCMD Model.

    Parameters
    ----------
    model : :obj:`bayescmd.bcmdModel.ModelBCMD`
        An initialised instance of a ModelBCMD class.

    Returns
    -------
    output : :obj:`dict`
        Dictionary of parsed model output.

    """

    model.create_initialised_input()

    model.run_from_buffer()

    output = model.output_parse()
    return output


def get_output(model_name,
               p,
               times,
               input_data,
               d0,
               targets,
               distance='euclidean',
               zero_flag=None):
    """Generate model output and distances.

    Parameters
    ----------
    model_name : :obj:`str`
        Name of model
    p : :obj:`dict`
        Dict of form {'parameter': value} for which posteriors are being
        investigated.
    times : :obj:`list` of :obj:`float`
        List of times at which the data was collected.
    input_data : :obj:`dict`
        Dictionary of input data as generated by :obj:`abc.inputParse`.
    d0 : :obj:`dict`
        Dictionary of real data, as generated by :obj:`abc.import_actual_data`.
    targets : :obj:`list` of :obj:`str`
        List of model outputs against which the model is being optimised.
    distance : :obj:`str`
        Distance measure. One of 'euclidean', 'manhattan', 'MAE', 'MSE'.
    zero_flag : dict
        Dictionary of form target(:obj:`str`): bool, where bool indicates
        whether to zero that target.

        Note: zero_flag keys should match targets list.

    Returns
    -------
    :obj:`tuple`
        A tuple of (p, model output data).

    """
    _model = ModelBCMD(
        model_name, inputs=input_data, params=p, times=times, outputs=targets, suppress=True)

    output = run_model(_model)

    dist = get_distance(
        d0,
        output,
        targets,
        distance=distance.split("_")[-1],
        zero_flag=zero_flag)

    try:
        for k, v in dist.items():
            p[k] = v
    except AttributeError as e:
        print("Error in finding distance.\n dist is {}:".format(dist))
        pprint.pprint(p)
        pprint.pprint(output)

        raise e

    if zero_flag:
        for k, boolean in zero_flag.items():
            if boolean:
                output[k] = [x - output[k][0] for x in output[k]]
    return p, output


# In[10]:


def get_repeated_outputs(df,
                         model_name,
                         parameters,
                         input_path,
                         inputs,
                         targets,
                         n_repeats,
                         zero_flag,
                         tolerance=None,
                         limit=None,
                         frac=None,
                         openopt_path=None,
                         offset=None,
                         distance='euclidean',
                         legend_model=None):
    """Generate model output and distances multiple times.

    Parameters
    ----------
    model_name : :obj:`str`
        Names of model. Should match the modeldef file for model being generated
        i.e. model_name of 'model`' should have a modeldef file
        'model1.modeldef'.
    parameters : :obj:`dict` of :obj:`str`: :obj:`tuple`
        Dict of model parameters to compare, with value tuple of the prior max
        and min.
    input_path : :obj:`str`
        Path to the true data file
    inputs : :obj:`list` of :obj:`str`
        List of model inputs.
    targets : :obj:`list` of :obj:`str`
        List of model outputs against which the model is being optimised.
    n_repeats : :obj: `int`
        Number of times to generate output data
    frac : :obj:`float`
        Fraction of results to consider. Should be given as a percentage i.e.
        1=1%, 0.1=0.1%
    zero_flag : dict
        Dictionary of form target(:obj:`str`): bool, where bool indicates
        whether to zero that target.

        Note: zero_flag keys should match targets list.
    openopt_path : :obj:`str` or :obj:`None`
        Path to the openopt data file if it exists. Default is None.
    offset : :obj:`dict`
        Dictionary of offset parameters if they are needed
    distance : :obj:`str`, optional
        Distance measure. One of 'euclidean', 'manhattan', 'MAE', 'MSE'.

    Returns
    -------
    fig : :obj:`matplotlib.figure`
        Figure containing all axes.

    """
    p_names = list(parameters.keys())
    sorted_df = df.sort_values(by=distance)

    if tolerance:
        accepted_limit = sum(df[distance].values < tolerance)
    elif limit:
        accepted_limit = limit
    elif frac:
        accepted_limit = frac_calculator(sorted_df, frac)
    else:
        raise ValueError('No limit or fraction given.')

    df_list = []
    if n_repeats > accepted_limit:
        print(
            "Setting number of repeats to quarter of the posterior size\n",
            file=sys.stderr)
        n_repeats = int(accepted_limit / 4)
    d0 = import_actual_data(input_path)
    input_data = inputParse(d0, inputs)

    true_data = pd.read_csv(input_path)
    times = true_data['t'].values

    if openopt_path:
        openopt_data = pd.read_csv(openopt_path)

    if n_repeats > accepted_limit:
        raise ValueError(
            "Number of requested model runs greater than posterior size:"
            "\n\tPosterior Size: {}\n\tNumber of runs: {}".format(
                accepted_limit, n_repeats))

    rand_selection = list(range(accepted_limit))
    random.shuffle(rand_selection)

    outputs_list = []

    posteriors = sorted_df.iloc[:accepted_limit][p_names].values
    select_idx = 0
    with Timer("Getting outputs"):
        while len(outputs_list) < n_repeats:
            try:
                idx = rand_selection.pop()
                p = dict(zip(p_names, posteriors[idx]))
                if offset:
                    p = {**p, **offset}
                output = get_output(
                    model_name,
                    p,
                    times,
                    input_data,
                    d0,
                    targets,
                    distance=distance,
                    zero_flag=zero_flag)
                outputs_list.append(output)
                print("Sample {}, idx:{}".format(len(outputs_list), idx))

            except (TimeoutError, TimeoutExpired) as e:
                print("Timed out for Sample {}, idx:{}".format(
                    len(outputs_list), idx))
                pprint.pprint(p)
                rand_selection.insert(0, idx)
            except (CalledProcessError) as e:
                print("CalledProcessError for Sample {}, idx:{}".format(
                    len(outputs_list), idx))
                pprint.pprint(p)
                rand_selection.insert(0, idx)

    d = {"Errors": {}, "Outputs": {}}
    d['Errors']['Average'] = np.nanmean(
        [o[0]['TOTAL'] for o in outputs_list])
    for target in targets:
        d['Errors'][target] = np.nanmean(
            [o[0][target] for o in outputs_list])
        d['Outputs'][target] = [o[1][target] for o in outputs_list]

    for ii, target in enumerate(targets):
        x = [j for j in times for n in range(len(d['Outputs'][target]))]
        with Timer('Transposing {}'.format(target)):
            y = np.array(d['Outputs'][target]).transpose()
            y = y.ravel()
        with Timer("Crafting DataFrame for {}".format(target)):
            model_name_col = [legend_model]*len(x)
            target_col = [target]*len(x)
            df1 = pd.DataFrame(
                {"Time": x, "Posterior": y, "Model Name": model_name_col, "Output": target_col})
        with Timer("Appending dataframe for {}".format(target)):
            df_list.append(df1.copy())
            del df1
    return pd.concat(df_list), true_data

# In[ ]:


labels = {"t": "Time (sec)",
          "SaO2sup": "SaO2 (%)",
          "P_a": "ABP (mmHg)",
          "temp": "Temperature ($^{\circ}$C)",
               "TOI": "TOI (%)",
          "HbO2": "$\Delta$HbO$_2$ $(\mu M)$",
          "HHb": "$\Delta$HHb $(\mu M)$",
          "CCO": "$\Delta$CCO $(\mu M)$"
          }
LIM = 50000
combinations = [('bph0', 'LWP475'), ('bph0', 'LWP479'),
                ('bph1', 'LWP475'), ('bph1_1', 'LWP479'),
                ('bph2', 'LWP475'), ('bph2_1', 'LWP479'),
                ('bph4', 'LWP475'), ('bph4_1', 'LWP479')]


signals = ['CCO', 'HbO2', 'HHb']

# for fig_num, combo in enumerate(combinations):
#     DATASET=combo[1]
#     model_name=combo[0]
model_names = ['bph0', 'bph1', 'bph2', 'bph4']
df_dict = {k: None for k in model_names}
for model_name in model_names:
    DATASET = 'LWP475'

    print("Working on {} - {}".format(model_name, DATASET))
    # Set config and create figure path
    config = configuration[model_name][DATASET]['bayescmd_config']
    figPath = "/home/buck06191/Dropbox/phd/hypothermia/ABC/Figures/{}/{}/{}".format(
        model_name, DATASET, 'NRMSE')
    dir_util.mkpath(figPath)

    # Get posterior
    print("\tRunning SQL query")
    df_post = client.query(
        configuration[model_name][DATASET]['posterior_query']).to_dataframe()

    # Plot posterior predictive
    config["offset"] = {}
    print("\tGetting Posterior Predictive")
    legend_model = model_name.replace('_', '.').replace('4', '3').upper()
    with Timer("Getting outputs"):
        df_list, true_data = get_repeated_outputs(df_post, n_repeats=1000, limit=LIM,
                                                  distance='NRMSE', legend_model=legend_model, **config)
        df_dict[model_name] = df_list

ylabel_dict = {
    'CCO': 'CCO ($\mu M$)', 'HbO2': 'HbO$_2$ ($\mu M$)', 'HHb': 'HHb ($\mu M$)'}
all_outputs = pd.concat(list(df_dict.values()))
with Timer("Plotting line plot"):
    g = sns.FacetGrid(all_outputs, row='Output',
                      hue='Model Name', height=2.5, aspect=2, sharey=False)

    for ii, ax in enumerate(g.axes.flatten()):
        ax.plot(true_data['t'], true_data[signals[ii]], 'k', '-')

    g = (g.map_dataframe(sns.lineplot, x='Time', y='Posterior')).add_legend()
    plt.setp(g._legend.get_title(), fontsize=12)
    plt.setp(g._legend.get_texts(), fontsize=11)
    g = g.set_titles('')
    g = g.set_xlabels('Time (sec)', fontsize=12)
    for ii, ax in enumerate(g.axes.flatten()):
        ax.set_ylabel(ylabel_dict[signals[ii]], fontsize=12)
        y_max = max(all_outputs[all_outputs['Output']
                                == signals[ii]]['Posterior'].max(), true_data[signals[ii]].max())
        y_min = min(all_outputs[all_outputs['Output']
                                == signals[ii]]['Posterior'].min(), true_data[signals[ii]].min())
        ax.set_yticks(np.linspace(y_min, y_max, 5))
        ax.set_yticklabels(["{:.2g}".format(y)
                            for y in np.linspace(y_min, y_max, 5)], fontdict={'fontsize': 11})
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=11)
g.fig.subplots_adjust(hspace=0.09)

g.savefig('/home/buck06191/Dropbox/phd/hypothermia/ABC/Figures/LWP475_joint_postpred.png',
          dpi=250, bbox_inches='tight', transparent=True)

#     for ix, ax in enumerate(axes.flatten()):
#         ax.set_ylabel(labels[signals[ix]])
#         old_title = ax.get_title().split(':')
#         new_title = ":".join([labels[signals[ix]].split()[0], old_title[1]])
#         ax.set_title(new_title, size=11)
#     axes.flatten()[-1].set_xlabel(labels['t'])
#     fig.suptitle(string.ascii_lowercase[fig_num]+")", ha='left', x=-0.02, y=0.925)
#fig.set_size_inches(18.5, 12.5)
#     with open(os.path.join(figPath, 'posterior_predictive_{}_{}.pickle'.format(model_name, DATASET)), 'wb') as f:
#         pickle.dump(fig, f)
#     fig.savefig(
#         os.path.join(figPath, 'posterior_predictive_{}_{}.png'
#                      .format(model_name, DATASET)),
#         bbox_inches='tight', bbox_extra_artists=(lgd,), dpi=250)
#     plt.close('all')


# In[ ]:


df_dict
