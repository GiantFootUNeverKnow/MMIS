#!/usr/bin/python
import numpy as np
import bisect
import logging
from job import Job

log = logging.getLogger("MMISLogger")

class Machine(object):

    def __init__(self, alpha1, alpha2, number):
        self.number = number
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.total_value = 0
        self.job_name = None
        self.work_start = None
        self.work_end = None
        self.current_job_yfactor = 0
        self.current_job_value = 0

    def clear(self):
        self.total_value = 0
        self.unload_job()

    def load_job(self, job):
        self.job_name = job.name
        self.work_start = job.arrival
        self.work_end = job.arrival + job.duration
        self.current_job_value = job.value
        self.current_job_yfactor = job.yfactor

    def is_idle(self):
        return (self.job_name == None)

    def unload_job(self):
        self.job_name = None
        self.current_job_value = 0
        self.current_job_yfactor = 0
        self.work_start = None
        self.work_end = None

    def start_job(self, job):
        if (job is not None):
            self.load_job(job)
            log.debug( "Job " + str(self.job_name) + " is on machine " + str(self.number) )
        else:
            raise RuntimeError("Invalid Job is given on Machine %d" % (self.number))

    def finish_job(self):
        if (self.current_job_value > 0):
            log.debug( "Machine " + str(self.number) + " finished job " + str(self.job_name) )
            self.total_value += self.current_job_value
            self.unload_job()
        else:
            raise RuntimeError("No job can be finished on Machine %d" % (self.number))

# Time always increments by amount of TIME_INCREMENT
# TIME_INCREMENT should be greater than EPSILON
TIME_INCREMENT = 1
EPSILON = 0.000001
NUM_MECHANISMS = 9
NUM_DETERMINISTIC_MECHANISMS = 3

class Scheduler(object):
    '''
    Scheduler can work in different abortion mechanisms. Currently these mechanisms are available. 
    If new abortion mechanisms were added, please modify this comment
    1. Abort according to priority
    2. Abort by chance
    3. Abort the least value job 
    4. Mechanism 1 + randomized dicider says YES
    5. Mechanism 2 + randomized dicider says YES
    6. Mechanism 3 + randomized dicider says YES
    7. Mechanism 1 OR randomized dicider says YES
    8. Mechanism 2 OR randomized dicider says YES
    9. Mechanism 3 OR randomized dicider says YES
    '''

    def __init__(self):
        self.machines = []
        self.mechanism = 0
        self.jobs = np.array([])
        self.experiment_counter = 0
        self.clear()
        
    def clear(self):
        self.time = -1
        self.experiment_counter += 1
        for machine in self.machines:
            machine.clear()
        for job in self.jobs:
            job.set_yfactor()

    def setup_machines_ui(self):
        print "Machines are prepared to be set up"
        n = int(raw_input("How many machines do you need? "))
        while (n <= 0):
            n = int(raw_input("Invalid number of machines. Please reenter: "))
        for i in range(n):
            alpha1 = float(raw_input("Please give first abortion ratio to machine %d: " % i))
            alpha2 = float(raw_input("Please give second abortion ratio to machine %d: " % i))
            while (alpha1 <= 0 or alpha2 <= 0):
                alpha1 = float(raw_input("Please give first abortion ratio to machine %d: " % i))
                alpha2 = float(raw_input("Please give second abortion ratios to machine %d: " % i))
            machine = Machine(alpha1, alpha2, i)
            self.machines.append(machine)
        print "There are three mechanism at this point: " 
        print "1. Abort according to priority"
        print "2. Abort by chance"
        print "3. Abort the least value job"
        print "4. Mechanism 1 + randomized dicider says YES"
        print "5. Mechanism 2 + randomized dicider says YES"
        print "6. Mechanism 3 + randomized dicider says YES"
        print "7. Mechanism 1 OR randomized dicider says YES"
        print "8. Mechanism 2 OR randomized dicider says YES"
        print "9. Mechanism 3 OR randomized dicider says YES"
        self.mechanism = int(raw_input("Which mechanism would you prefer? "))
        while (n <= 0 or n > NUM_MECHANISMS):
            self.mechanism = int(raw_input("Which mechanism would you prefer? "))
        if (self.mechanism > NUM_DETERMINISTIC_MECHANISMS):
            print "Please input randomized dicider function in the format\"lambda y: <function expression with respect to y>\""
            self.randomized_dicider = eval(raw_input("Function:"))
        print "Machines finished setup"

        log.debug("Machines are setup")

    def setup_machines_file(self, filename):
        with open(filename) as f:
            n = int(f.readline())
            for i in range(n):
                line = f.readline().split()
                [alpha1, alpha2] = [int(j) for j in line]
                machine = Machine(alpha1, alpha2, i)
                self.machines.append(machine)
            self.mechanism = int(f.readline())
            
            randomized_dicider_exp = f.readline()
            if (randomized_dicider_exp != ""):
                self.randomized_dicider = eval(randomized_dicider_exp)

        log.debug("Machines are setup")

    def select_dataset_file(self, filename):
        jobs_matrix = np.loadtxt(filename)
        log.debug(jobs_matrix)
        jobs = [Job.deserializeJob(job) for job in jobs_matrix]
        self.jobs = np.array(sorted(jobs, key = lambda x: x.arrival)) 

        log.debug("Dataset file %s has been loaded", filename)

    def select_dataset_ui(self):
        filename = raw_input("Please choose a set of jobs: ")
        self.select_dataset_file(filename)

    def regular_check(self):
        self.time += TIME_INCREMENT
        for machine in self.machines:
            if ( not machine.is_idle() and self.time == machine.work_end):
                machine.finish_job()

    def heuristic1(self, job):
        log.debug( "heuristic1 has %d at time %d" % (job.name, self.time ) ) 
        # Assume priority of mahcines are ordered by their indices
        for i in range(len(self.machines)):
            machine = self.machines[i]
            if (job.value >= machine.current_job_value * machine.alpha1):
                self.machines[i].start_job(job)
                return

    def heuristic2(self, job):
        log.debug( "heuristic2 has %d at time %d" % (job.name, self.time ) )
        low_wage_machines = [machine for machine in self.machines 
            if (job.value >= machine.current_job_value * machine.alpha1)]
        if (low_wage_machines != []):
            return np.random.choice(low_wage_machines).start_job(job)

    def heuristic3(self, job):
        log.debug( "heuristic3 has %d at time %d" % (job.name, self.time ))
        lowest_wage_machine = None
        for machine in self.machines:
            if (job.value >= machine.current_job_value * machine.alpha1):
                if (lowest_wage_machine is None or 
                    lowest_wage_machine.current_job_value > machine.current_job_value):
                    lowest_wage_machine = machine
        if lowest_wage_machine is not None:
            lowest_wage_machine.start_job(job)

    def heuristic4(self, job):
        log.debug( "heuristic4 has %d at time %d" % (job.name, self.time ))
        # Assume priority of mahcines are ordered by their indices
        for i in range(len(self.machines)):
            machine = self.machines[i]
            if (job.value >= machine.current_job_value * machine.alpha1
                and job.yfactor * job.value >= machine.current_job_yfactor * machine.current_job_value * machine.alpha2):
                self.machines[i].start_job(job)
                return
 
    def heuristic5(self, job):
        log.debug( "heuristic5 has %d at time %d" % (job.name, self.time ))
        low_wage_machines = [machine for machine in self.machines 
            if (job.value >= machine.current_job_value * machine.alpha1)
            and (job.yfactor * job.value >= machine.current_job_yfactor * machine.current_job_value * machine.alpha2)]
        if (low_wage_machines != []):
            return np.random.choice(low_wage_machines).start_job(job)
 
    def heuristic6(self, job):
        log.debug( "heuristic6 has %d at time %d" % (job.name, self.time ))
        lowest_wage_machine = None
        for machine in self.machines:
            if (job.value >= machine.current_job_value * machine.alpha1
               and job.yfactor * job.value >= machine.current_job_yfactor * machine.current_job_value * machine.alpha2):
                if (lowest_wage_machine is None or 
                    lowest_wage_machine.current_job_value > machine.current_job_value):
                    lowest_wage_machine = machine
        if lowest_wage_machine is not None:
            lowest_wage_machine.start_job(job)
     
    def heuristic7(self, job):
        log.debug( "heuristic7 has %d at time %d" % (job.name, self.time ))
        # Assume priority of mahcines are ordered by their indices
        for i in range(len(self.machines)):
            machine = self.machines[i]
            if (job.value >= machine.current_job_value * machine.alpha1
                or job.yfactor * job.value >= machine.current_job_yfactor * machine.current_job_value * machine.alpha2):
                self.machines[i].start_job(job)
                return
  
    def heuristic8(self, job):
        log.debug( "heuristic8 has %d at time %d" % (job.name, self.time ))
        low_wage_machines = [machine for machine in self.machines 
            if (job.value >= machine.current_job_value * machine.alpha1)
            or (job.yfactor * job.value >= machine.current_job_yfactor * machine.current_job_value * machine.alpha2)]
        if (low_wage_machines != []):
            return np.random.choice(low_wage_machines).start_job(job)
     
    def heuristic9(self, job):
        log.debug( "heuristic9 has %d at time %d" % (job.name, self.time ))
        lowest_wage_machine = None
        for machine in self.machines:
            if (job.value >= machine.current_job_value * machine.alpha1
               or job.yfactor * job.value >= machine.current_job_yfactor * machine.current_job_value * machine.alpha2):
                if (lowest_wage_machine is None or 
                    lowest_wage_machine.current_job_value > machine.current_job_value):
                    lowest_wage_machine = machine
        if lowest_wage_machine is not None:
            lowest_wage_machine.start_job(job)
  
    def process_job(self, job):
        function_name = "self.heuristic" + str(self.mechanism)
        eval(function_name)(job)

    def run_schedule(self):
        log.debug( "Start running schedules" )
        
        n = len(self.jobs)
        index = 0
        while (index < n):
            self.regular_check()
            while (index < n and abs(self.jobs[index].arrival - self.time ) < EPSILON):
                # The while loop is for simultaneous jobs
                self.process_job(self.jobs[index])
                index += 1
        
        # We can expect current jobs on the machines can all be done 
        for machine in self.machines:
            if (not machine.is_idle()):
                machine.finish_job()
        
    def get_result(self):
        return sum([machine.total_value for machine in self.machines])

    def offline_single_machine(self):
        opt = {-1: 0}
        prev = {-1: -1}
        n = len(self.jobs)
        reordered_jobs = sorted(self.jobs, key = lambda x: (x.arrival + x.duration))
        finishing_times = [job.arrival + job.duration for job in reordered_jobs]
        for i in range(n): 
            prev[i] = bisect.bisect_right(finishing_times, reordered_jobs[i].arrival) - 1
        for i in range(n):
            opt[i] = max([reordered_jobs[i].value + opt[prev[i]], opt[i-1]]) 
        return opt[n-1]

    def show_result_ui(self):
        print "-----------------------------------------------------"
        print "Result of experiment %d:" % (self.experiment_counter)
        payoff = 0
        for machine in self.machines:
            print "Machine %d earned %d" % (machine.number, machine.total_value)
            payoff += machine.total_value
        print "Totally, we earned %d" % payoff
        print "-----------------------------------------------------"

    def schedule(self, repetition = 1):
        payoff = 0
        for i in range(repetition):
            self.run_schedule()
            self.show_result_ui()
            payoff += self.get_result()
            self.clear()
        expected_payoff = payoff * 1.0 / repetition
        print "****************************************************"
        print "Expected payoff: %d" % expected_payoff 
        offline_optimal = self.offline_single_machine()
        print "The optimal reward that can be obtained for this job sequence is ", offline_optimal
        print "The competitive ratio is ", offline_optimal * 1.0 / expected_payoff
        print "****************************************************"
        return expected_payoff

    # TODO: add an accumulator to record the worst case
