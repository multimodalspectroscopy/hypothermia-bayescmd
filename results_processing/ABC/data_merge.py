"""Combine parameter files."""
import os
import argparse


from bayescmd.results_handling import data_merge_by_batch


ap = argparse.ArgumentParser('Choose results to process:')
ap.add_argument(
    'parent_dir',
    metavar="PARENT_DIR",
    help='Parent directory holding model run folders')

args = ap.parse_args()
datasets = ['LWP475', 'LWP479', 'LWP481', 'LWP484']
for dataset in datasets:
    pfile = data_merge_by_batch(os.path.join(args.parent_dir, dataset))
