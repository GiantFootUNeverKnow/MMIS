#!/usr/bin/python
import numpy as np

class Machine(object):
    '''
    Machine states can be either idle or busy. If any other states are added, please modify here
        0 -> idle
        1 -> busy
    '''

    def __init__(self, alpha, number):
        self.number = number
        self.alpha = alpha
        self.total_value = 0
        self.state = 0
        self.job = None
        self.work_start = None
        self.work_end = None
        self.current_job_value = None

    def turn_on(self):
        self.state = 1

    def turn_off(self):
        self.state = 0

    def load_job(self, job):
        turn_on()
        self.job = job
        self.work_start = job.arrival
        self.work_end = job.arrival + job.duration
        self.current_job_value = job.value

    def unload_job(self, job):
        self.job = None
        self.current_job_value = None
        self.work_start = None
        self.work_end = None
        turn_off()

    def start_job(self, job):
        if (job is not None):
            load_job(job)
        else:
            raise Error("Invalid Job is given on Machine %d" % (self.number))

    def finish_job(self):
        if (self.state):
            self.total_value += self.current_job_value
        else:
            raise Error("No job can be finished on Machine %d" & (self.number))

class Scheduler(object):
    '''
    Scheduler can work in different abortion mechanisms. Currently these mechanisms are available. 
    If new abortion mechanisms were added, please modify this comment
    1. Abort according to priority
    2. Abort by chance
    3. Abort the least value job 
    '''

    def __init__(self):
        self.machines = []
        self.mechanism = 0

    def setup_machines(self):
        print "Machines are prepared to be set up"
        n = int(raw_input("How many machines do you need? "))
        while (n <= 0):
            n = int(raw_input("Invalid number of machines. Please reenter: "))
        for i in range(n):
            alpha = float(raw_input("Please give abortion ratio to machine %d: " % i))
            while (alpha <= 0):
                alpha = float(raw_input("Please give abortion ratio to machine %d: " % i))
            machine = Machine(alpha, i)
            self.machines.append(machine)
        print "There are three mechanism at this point: " 
        print "1. Abort according to priority"
        print "2. Abort by chance"
        print "3. Abort the least value job"
        self.mechanism = int(raw_input("Which mechanism would you prefer? "))
        print "Machines finished setup"

    def run_schedule(self):
        print "Start running schedules"

    def select_dataset(self):
        filename = raw_input("Please choose a set of jobs: ")
        jobs = np.loadtxt(filename)
        print jobs
        jobs = np.array(sorted(jobs, key = lambda x: x[0]))
        return jobs

    def show_result(self):
        print "-----------------------------------------------------"
        print "Result of experiment:"
        payoff = 0
        for machine in self.machines:
            print "Machine %d earned %d" % (machine.number, machine.total_value)
            payoff += machine.total_value
        print "Totally, we earned ", payoff

def main():
    scheduler = Scheduler()
    scheduler.setup_machines()
    scheduler.select_dataset()
    scheduler.run_schedule()
    scheduler.show_result()

if __name__ == "__main__":
    main();
