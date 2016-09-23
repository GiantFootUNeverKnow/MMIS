#!/usr/bin/python
import logging
import sys
import argparse
from scheduler import Scheduler

log = logging.getLogger("MMISLogger")
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

parser = argparse.ArgumentParser();
parser.add_argument('--debug', action='store_const', const=True, default=False, help='Enable logging of debug message')
parser.add_argument('--experiment', help='This argument will switch to batch experiment mode, please specify a configuration file. Also, the option --jb must be used in experiment mode')
parser.add_argument('--jb', help='Specify the job base')

args = parser.parse_args()
if args.debug:
    log.setLevel(logging.DEBUG)

def main():
    scheduler = Scheduler()
    if args.experiment:
        config = args.experiment
        print config
        if args.jb is None:
            raise NameError("Please use --jb to specify the job base")
        print args.jb
    else:
        scheduler.setup_machines()
        scheduler.select_dataset()
        scheduler.run_schedule()
        scheduler.show_result()

if __name__ == "__main__":
    main();
