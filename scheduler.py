#!/usr/bin/python
import numpy as np

'''
Job data is a 4-tuple: (arrival, duration, value, index)
'''

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
        self.job = job[3]
        self.work_start = job[0]
        self.work_end = job.arrival + job[1]
        self.current_job_value = job[2]

    def unload_job(self):
        self.job = None
        self.current_job_value = None
        self.work_start = None
        self.work_end = None
        self.turn_off()

    def start_job(self, job):
        if (job is not None):
            self.oad_job(job)
            print "Job " + self.job + " is on machine " + self.number
        else:
            raise Error("Invalid Job is given on Machine %d" % (self.number))

    def finish_job(self):
        if (self.state):
            print "Machine " + self.number + " finished job " + self.job
            self.unload_job()
            self.total_value += self.current_job_value
        else:
            raise Error("No job can be finished on Machine %d" & (self.number))

# Time always increments by amount of TIME_INCREMENT
# TIME_INCREMENT should be greater than EPSILON
TIME_INCREMENT = 1
EPSILON = 0.000001

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
        self.time = -1

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

    def regular_check(self):
        self.time += TIME_INCREMENT
        for machine in self.machines:
            if (machine.state and self.time == machine.work_end):
                machine.finish_job()
   
    def heuristic1(self, job):
        print "heuristic1 has %d at time %d" % (job[3], self.time ) 

    def heuristic2(self, job):
        print "heuristic2 has %d at time %d" % (job[3], self.time )

    def heuristic3(self, job):
        print "heuristic3 has %d at time %d" % (job[3], self.time )

    def process_job(self, job):
        function_name = "self.heuristic" + str(self.mechanism)
        eval(function_name)(job)

    def run_schedule(self):
        print "Start running schedules"
        
        n = len(self.jobs)
        index = 0
        while (index < n):
            self.regular_check()
            while (index < n and abs(self.jobs[index][0] - self.time ) < EPSILON):
                self.process_job(self.jobs[index])
                index += 1

    def select_dataset(self):
        filename = raw_input("Please choose a set of jobs: ")
        jobs = np.loadtxt(filename)
        print jobs
        self.jobs = np.array(sorted(jobs, key = lambda x: x[0])) 

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
