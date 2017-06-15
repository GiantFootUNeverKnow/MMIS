#!/usr/bin/python
import numpy as np
import bisect
import logging
import random
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
        self.randomized_decider = None

    def clear(self):
        self.total_value = 0
        self.unload_job()

    def load_job(self, job):
        self.job_name = job.name
        self.work_start = job.arrival
        self.work_end = job.arrival + job.duration
        self.current_job_value = job.value
        self.current_job_yfactor = job.yfactor

    def set_randomized_decider(self, randomized_decider):
        self.randomized_decider = randomized_decider

    def is_idle(self):
        return (self.job_name == None)

    def is_replaceable(self, coming_job):
        return coming_job.value + EPSILON >= self.current_job_value * self.alpha1 

    def is_replaceable_SRD(self, coming_job):
        assert self.randomized_decider is not None
        
        return (self.randomized_decider(coming_job.yfactor) + EPSILON >= 
               self.randomized_decider(self.current_job_yfactor))

    def is_replaceable_RD(self, coming_job):
        assert self.randomized_decider is not None

        return (self.randomized_decider(coming_job.yfactor) * coming_job.value + EPSILON >= 
            self.randomized_decider(self.current_job_yfactor) * self.current_job_value * self.alpha2)  

    def unload_job(self):
        self.job_name = None
        self.current_job_value = 0
        self.current_job_yfactor = 0
        self.work_start = None
        self.work_end = None

    def start_job(self, job):
        if (job is not None):
            self.load_job(job)
            log.debug( "Job " + str(self.job_name) + " is on machine " + str(self.number) + " at time " + str(self.work_start))
        else:
            raise RuntimeError("Invalid Job is given on Machine %d" % (self.number))

    def finish_job(self):
        if (self.current_job_value > 0):
            log.debug( "Machine " + str(self.number) + " finished job " + str(self.job_name) + " at time " + str(self.work_end))
            self.total_value += self.current_job_value
            self.unload_job()
        else:
            raise RuntimeError("No job can be finished on Machine %d" % (self.number))

# TIME_INCREMENT should be greater than EPSILON
EPSILON = 0.000001
NUM_MECHANISMS = 13
MECHANISMS_WITH_RD = [4, 5, 6, 7, 8, 9, 12] 

class Scheduler(object):
    '''
    Scheduler can work in different abortion mechanisms. Currently these mechanisms are available. 
    If new abortion mechanisms were added, please modify this comment
    1. Abort according to priority
    2. Abort by chance
    3. Abort the least value job 
    4. Mechanism 1 + randomized decider says YES
    5. Mechanism 2 + randomized decider says YES
    6. Mechanism 3 + randomized decider says YES
    7. Mechanism 1 OR randomized decider says YES
    8. Mechanism 2 OR randomized decider says YES
    9. Mechanism 3 OR randomized decider says YES
    10. (Single Machine) Randomly select one abortion ratio from two ratio on the machine 
    11. (Single Machine) Randomly decide whether we abort
    12. Mechanism 1 + simplified randomized decider says YES 
    13. (1 or 2 machines) Cooperative Greedy Algorithm
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
        print "4. Mechanism 1 + randomized decider says YES"
        print "5. Mechanism 2 + randomized decider says YES"
        print "6. Mechanism 3 + randomized decider says YES"
        print "7. Mechanism 1 OR randomized decider says YES"
        print "8. Mechanism 2 OR randomized decider says YES"
        print "9. Mechanism 3 OR randomized decider says YES"
        print "10. (Single Machine) Randomly select one abortion ratio from two ratio on the machine"  
        print "11. (Single Machine) Randomly decide whether to abort"
        print "12. Mechanism 1 + simplified randomized decider says YES" 
        print "13. (1 or 2 machines) Cooperative Greedy Algorithm"
        self.mechanism = int(raw_input("Which mechanism would you prefer? "))
        while (n <= 0 or n > NUM_MECHANISMS):
            self.mechanism = int(raw_input("Which mechanism would you prefer? "))
        if (self.mechanism in MECHANISMS_WITH_RD):
            for i in range(n):
                print "Please input randomized decider function for machine %d in the format\"lambda y: <function expression with respect to y>\"" % i
                self.machines[i].set_randomized_decider(eval(raw_input("Function:")))
        print "Machines finished setup"

        log.debug("Machines are setup")

    def setup_machines_file(self, filename):
        with open(filename) as f:
            n = int(f.readline())
            for i in range(n):
                line = f.readline().split()
                [alpha1, alpha2] = [float(j) for j in line]
                machine = Machine(alpha1, alpha2, i)
                self.machines.append(machine)
            self.mechanism = int(f.readline())
           
            for i in range(n):
                randomized_decider_exp = f.readline()
                if (randomized_decider_exp != ""):
                    self.machines[i].set_randomized_decider(eval(randomized_decider_exp))

        log.debug("Machines are setup")

    # We assume the incoming jobs are always in the order of their arrival time
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
        for machine in self.machines:
            if ( not machine.is_idle() and self.time >= machine.work_end):
                machine.finish_job()

    def heuristic1(self, job):
        log.debug( "heuristic1 has %d at time %d" % (job.name, self.time ) ) 
        # Assume priority of mahcines are ordered by their indices
        for i in range(len(self.machines)):
            machine = self.machines[i]
            if machine.is_replaceable(job): 
                machine.start_job(job)
                return

    def heuristic2(self, job):
        log.debug( "heuristic2 has %d at time %d" % (job.name, self.time ) )
        candidates = [machine for machine in self.machines 
            if (machine.is_replaceable(job))]
        if (candidates != []):
            return np.random.choice(candidates).start_job(job)

    def heuristic3(self, job):
        log.debug( "heuristic3 has %d at time %d" % (job.name, self.time ))
        lowest_wage_machine = None
        for machine in self.machines:
            if (machine.is_replaceable(job)):
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
            if (machine.is_replaceable(job)
                and machine.is_replaceable_RD(job)):
                machine.start_job(job)
                return
 
    def heuristic5(self, job):
        log.debug( "heuristic5 has %d at time %d" % (job.name, self.time ))
        candidates = [machine for machine in self.machines 
            if (machine.is_replaceable(job))
            and (machine.is_replaceable_RD(job))]
        if (candidates != []):
            return np.random.choice(candidates).start_job(job)
 
    def heuristic6(self, job):
        log.debug( "heuristic6 has %d at time %d" % (job.name, self.time ))
        lowest_wage_machine = None
        for machine in self.machines:
            if (machine.is_replaceable(job)
               and machine.is_replaceable_RD(job)):
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
            if (machine.is_replaceable(job)
                or machine.is_replaceable_RD(job)):
                machine.start_job(job)
                return
  
    def heuristic8(self, job):
        log.debug( "heuristic8 has %d at time %d" % (job.name, self.time ))
        candidates = [machine for machine in self.machines 
            if (machine.is_replaceable(job))
                or (machine.is_replaceable_RD(job))]
        if (candidates != []):
            return np.random.choice(candidates).start_job(job)
     
    def heuristic9(self, job):
        log.debug( "heuristic9 has %d at time %d" % (job.name, self.time ))
        lowest_wage_machine = None
        for machine in self.machines:
            if (machine.is_replaceable(job)
               or machine.is_replaceable_RD(job)):
                if (lowest_wage_machine is None or 
                    lowest_wage_machine.current_job_value > machine.current_job_value):
                    lowest_wage_machine = machine
        if lowest_wage_machine is not None:
            lowest_wage_machine.start_job(job)
 
    def heuristic10(self, job):
        # This mechanism is only allowed to run on single machine now, running heuristic10 on multiple machines does not make sense yet
        assert len(self.machines) == 1
        log.debug( "heuristic10 has %d at time %d" % (job.name, self.time ))       
        machine = self.machines[0]
        alpha = np.random.choice([machine.alpha1, machine.alpha2])
        if (job.value + EPSILON >= machine.current_job_value * alpha):
            machine.start_job(job)

    def heuristic11(self, job):
        # This mechanism is only allowed to run on single machine now, running heuristic11 on multiple machines does not make sense yet
        assert len(self.machines) == 1
        log.debug( "heuristic11 has %d at time %d" % (job.name, self.time ))
        machine = self.machines[0]
        is_start = np.random.randint(2)
        if (is_start):
            machine.start_job(job)
    
    def heuristic12(self, job):
        log.debug( "heuristic12 has %d at time %d" % (job.name, self.time ))
        # Assume priority of mahcines are ordered by their indices
        for i in range(len(self.machines)):
            machine = self.machines[i]
            if (machine.is_replaceable(job)
                and machine.is_replaceable_SRD(job)):
                machine.start_job(job)
                return

    def heuristic13(self, job):
        # This mechanism is only allowed to run on 1 or 2 machines, running heuristic13 on more than 2 machines do not make sense yet
        assert len(self.machines) == 1 or len(self.machines) == 2
        log.debug( "heuristic13 has %d at time %d" % (job.name, self.time))
        if (len(self.machines) == 1 and not hasattr(self.machines[0], 'primary')):
            machine1 = self.machines[0]
            machine2 = Machine(machine1.alpha1, machine1.alpha2, 2)
            machine2.destroy_token = True
            self.machines.append(machine2)
            machine1.primary = np.random.choice([True, False])
            machine1.phase_end = 0
        elif (not hasattr(self.machines[0], 'primary')): # There exist two machines
            machine1 = self.machines[0]
            machine2 = self.machines[1]
            machine1.primary = False
            machine1.phase_end = 0
        else:
            machine1 = self.machines[0]
            machine2 = self.machines[1]
        if (job.arrival >= machine1.phase_end):
            machine1.primary = not machine1.primary
            PM = machine1 if machine1.primary else machine2
            machine1.phase_end = job.arrival + job.duration if PM.is_idle() else PM.work_end
        PM = machine1 if machine1.primary else machine2
        SM = machine1 if not machine1.primary else machine2
        if (PM.is_idle()):
            PM.start_job(job)
        elif (SM.is_replaceable(job)):
            SM.start_job(job)

    def process_job(self, job):
        function_name = "self.heuristic" + str(self.mechanism)
        eval(function_name)(job)

    def run_schedule(self):
        log.debug( "Start running schedules" )
        
        n = len(self.jobs)
        index = 0
        while (index < n):
            self.time = self.jobs[index].arrival
            self.regular_check()
            self.process_job(self.jobs[index])
            index += 1
        
        # We can expect current jobs on the machines can all be done 
        for machine in self.machines:
            if (not machine.is_idle()):
                machine.finish_job()
        
    def get_result(self):
        return sum([machine.total_value for machine in self.machines])
    
    def _order_job_by_finishing_time(self, jobs):
        return sorted(self.jobs, key = lambda x: (x.arrival + x.duration))

    def _calc_latest_previous_job(self, jobs):
        n = len(self.jobs)
        prev = {-1: -1}
        reordered_jobs = self._order_job_by_finishing_time(jobs)
        finishing_times = [job.arrival + job.duration for job in reordered_jobs]
        for i in range(n):
            prev[i] = bisect.bisect_right(finishing_times, reordered_jobs[i].arrival) - 1
        return prev

    def offline_single_machine(self):
        opt = {-1: 0}
        n = len(self.jobs)
        prev = self._calc_latest_previous_job(self.jobs)
        reordered_jobs = self._order_job_by_finishing_time(self.jobs)
        for i in range(n):
            opt[i] = max([reordered_jobs[i].value + opt[prev[i]], opt[i-1]]) 
        return opt[n-1]

    def offline_double_machine(self):
        n = len(self.jobs)
        opt = np.zeros((n+1, n+1))
        prev = self._calc_latest_previous_job(self.jobs)
        reordered_jobs = self._order_job_by_finishing_time(self.jobs)
        for i in range(1, n+1):
            opt[i, 0] = opt[0, i] = max([reordered_jobs[i - 1].value + opt[prev[i - 1] + 1, 0], opt[i - 1, 0]])
        for i in range(1, n+1):
            for j in range(1, n+1):
                if i > j:
                    opt[i, j] = max([opt[i-1, j], opt[prev[i - 1] + 1, j] + reordered_jobs[i - 1].value])
                elif i < j:
                    opt[i, j] = max([opt[i, j-1], opt[i, prev[j - 1] + 1] + reordered_jobs[j - 1].value])
                else:
                    opt[i, j] = max([opt[i-1, j-1], 
                                     opt[i - 1, prev[j - 1] + 1] + reordered_jobs[j - 1].value,
                                     opt[prev[i - 1] + 1, j - 1] + reordered_jobs[i - 1].value
                                    ])
        return opt[n, n] 

    def general_offline_optimal(self):
        raise NotImplementedError

    def calc_offline_optimal(self):
        n = len(self.machines);
        if (n == 1):
            return self.offline_single_machine()
        elif (n == 2):
            return self.offline_double_machine()
        else:
            return self.general_offline_optimal()

    def log_result(self):
        formatted_result = "Result of experiment " + str(self.experiment_counter) + ":\n"
        for machine in self.machines:
            formatted_result = formatted_result + "Machine " + str(machine.number) \
                + " earned " + str(machine.total_value) + "\n" 
        formatted_result = formatted_result + "Totally, we earned " + str(self.get_result()) \
                + "\n" + "-----------------------------------------------------" 
        log.info(formatted_result)

    def postprocess(self):
        # Remove imaginary machines produced during scheduling
        self.machines = [machine for machine in self.machines if (not hasattr(machine, 'destroy_token'))]
        # Remove primary mark
        for machine in self.machines:
            delattr(machine, 'primary')

    def schedule(self, repetition = 1, print_result = True):
        payoff = 0
        for i in range(repetition):
            self.run_schedule()
            self.postprocess()
            self.log_result()
            payoff += self.get_result()
            self.clear()
        expected_payoff = payoff * 1.0 / repetition
        offline_optimal = self.calc_offline_optimal() 
        competitive_ratio = offline_optimal * 1.0 / expected_payoff

        formatted_result = "Expected payoff: " + str(expected_payoff) \
            + "\n" + "The optimal reward that can be obtained for this job sequence is " + str(offline_optimal) \
            + "\n" + "The competitive ratio is " + str(competitive_ratio) \
            + "\n" + "****************************************************" 
        if (print_result):
            formatted_result = "****************************************************" + "\n" + formatted_result
            print formatted_result
        else:
            log.info(formatted_result) 
        
        return (expected_payoff, competitive_ratio, offline_optimal)


    # TODO: add an accumulator to record the worst case
