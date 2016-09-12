#!/usr/bin/python
import numpy as np
import logging

log = logging.getLogger("MMISLogger")

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
        self.turn_on()
        self.job = job[3]
        self.work_start = job[0]
        self.work_end = job[0] + job[1]
        self.current_job_value = job[2]

    def unload_job(self):
        self.job = None
        self.current_job_value = None
        self.work_start = None
        self.work_end = None
        self.turn_off()

    def start_job(self, job):
        if (job is not None):
            self.load_job(job)
            log.debug( "Job " + str(self.job) + " is on machine " + str(self.number) )
        else:
            raise Error("Invalid Job is given on Machine %d" % (self.number))

    def finish_job(self):
        if (self.state):
            log.debug( "Machine " + str(self.number) + " finished job " + str(self.job) )
            self.total_value += self.current_job_value
            self.unload_job()
        else:
            raise Error("No job can be finished on Machine %d" % (self.number))

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
        print "0. Vanilla (Never abort)"
        print "1. Abort according to priority"
        print "2. Abort by chance"
        print "3. Abort the least value job"
        self.mechanism = int(raw_input("Which mechanism would you prefer? "))
        print "Machines finished setup"

    def select_dataset(self):
        filename = raw_input("Please choose a set of jobs: ")
        jobs = np.loadtxt(filename)
        log.info(jobs)
        self.jobs = np.array(sorted(jobs, key = lambda x: x[0])) 

    def regular_check(self):
        self.time += TIME_INCREMENT
        for machine in self.machines:
            if (machine.state and self.time == machine.work_end):
                machine.finish_job()
   
    def check_idle_machines(self):
        for machine in self.machines:
            if (machine.state == 0):
                return machine
        return None

    def heuristic0(self, job):
        log.debug( "heuristic0 has %d at time %d" % (job[3], self.time) )
        return

    def heuristic1(self, job):
        log.debug( "heuristic1 has %d at time %d" % (job[3], self.time ) ) 
        # Assume priority of mahcines are ordered by their indices
        for i in range(len(self.machines)):
            if (job[2] > self.machines[i].current_job_value * self.machines[i].alpha):
                self.machines[i].start_job(job)
                return

    def heuristic2(self, job):
        log.debug( "heuristic2 has %d at time %d" % (job[3], self.time ) )
        low_wage_machines = [machine for machine in self.machines 
            if (job[2] > machine.current_job_value * machine.alpha)]
        if (low_wage_machines != []):
            return np.random.choice(low_wage_machines).start_job(job)

    def heuristic3(self, job):
        log.debug( "heuristic3 has %d at time %d" % (job[3], self.time ))
        lowest_wage_machine = None
        for machine in self.machines:
            if (job[2] > machine.current_job_value * machine.alpha):
                if (lowest_wage_machine is None or 
                    lowest_wage_machine.current_job_value > machine.current_job_value):
                    lowest_wage_machine = machine
        if lowest_wage_machine is not None:
            lowest_wage_machine.start_job(job)

    def process_job(self, job):
        idle_machine = self.check_idle_machines()
        if (idle_machine is not None):
            idle_machine.start_job(job)
        else:
            function_name = "self.heuristic" + str(self.mechanism)
            eval(function_name)(job)

    def run_schedule(self):
        log.info( "Start running schedules" )
        
        n = len(self.jobs)
        index = 0
        while (index < n):
            self.regular_check()
            while (index < n and abs(self.jobs[index][0] - self.time ) < EPSILON):
                # The while loop is for simultaneous jobs
                self.process_job(self.jobs[index])
                index += 1
        
        # We can expect current jobs on the machines can all be done 
        for machine in self.machines:
            if (machine.state):
                machine.finish_job()
            

    def show_result(self):
        print "-----------------------------------------------------"
        print "Result of experiment:"
        payoff = 0
        for machine in self.machines:
            print "Machine %d earned %d" % (machine.number, machine.total_value)
            payoff += machine.total_value
        print "Totally, we earned ", payoff

