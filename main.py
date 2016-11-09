#!/usr/bin/python
import logging
import os
import sys
import argparse
import numpy as np
from scheduler import Scheduler

log = logging.getLogger("MMISLogger")
out_hdlr = logging.StreamHandler(sys.stderr)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)
log.propagate = False

parser = argparse.ArgumentParser();
parser.add_argument('--debug', action='store_const', const=True, default=False, help='Enable logging of debug message')
parser.add_argument('--experiment', help='This argument will switch to batch experiment mode, please specify a configuration file. Also, the option --jb must be used in experiment mode')
parser.add_argument('--jb', help='Specify the job base. This option is only effective when the program starts in batch experiment mode. It expects a name of directory, without a slash. ')
parser.add_argument('--repeat', type=int, default= 1, help='This option would run the simulation for N times and calculate an expectation of the total payoff over results of n simulations; It is most useful to use this option for randomized algorithm')

args = parser.parse_args()
if args.debug:
    log.setLevel(logging.DEBUG)

def main():
    scheduler = Scheduler()
    if args.experiment:
        config = args.experiment
        job_base = args.jb
        if job_base is None:
            raise NameError("Please use --jb to specify the job job_base")
        scheduler.setup_machines_file(config)
        competitive_ratios = []
        for jobfile in os.listdir(job_base):
            scheduler.select_dataset_file(job_base + '/' + jobfile)
            _, competitive_ratio = scheduler.schedule(repetition = args.repeat)
            competitive_ratios.append(competitive_ratio)
        job_base_competitive_ratio_expectation = np.average(competitive_ratios)
        job_base_competitive_ratio_variance = np.var(competitive_ratios)
        print "Expectation of competitive ratios over the job base: ", job_base_competitive_ratio_expectation
        print "Variance of competitive ratios over the job base: ", job_base_competitive_ratio_variance
    else:
        scheduler.setup_machines_ui()
        scheduler.select_dataset_ui()
        scheduler.schedule(repetition = args.repeat)

if __name__ == "__main__":
    main();
