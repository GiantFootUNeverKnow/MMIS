#!/usr/bin/python

import numpy as np
import math
import os
import argparse
import time
from job import Job

parser = argparse.ArgumentParser();
parser.add_argument('--batch', action='store_const', const=True, default=False, help='Switch to batch mode. By default, all generated jobs will still be stored in the directory named after the generation scheme as usual, but we recommend you to use --redir to redirect batch jobs to a separate directory ')
parser.add_argument('--redir', help='Specify name of a directory to store the generated jobs')
parser.add_argument('--jl', help='Specify the length of a job sequence, which by default is set to 999', type=int, default=999)
args = parser.parse_args()

file_counter = 1
def get_file_counter():
    global file_counter
    file_counter += 1
    return file_counter - 1

"""
A general class for job generation scheme. Any variation of the scheme can be added as subclass of this class
start() is the entrance of any operations of a scheme
"""
class JobsGenerationScheme(object):

    # Abstract function that must be implemented in the subclass
    def get_helpinfo(self):
        # return description of the scheme
        raise NotImplementedError

    # Abstract function that must be implemented in the subclass
    def __init__(self):
        raise NotImplementedError

    # Abstract function that must be implemented in the subclass
    def generate(self):
        # Generate job sequence and return
        raise NotImplementedError

    # Abstract function that must be implemented in the subclass
    def set_parameter(self):
        # Prompt the user to enter necessary parameters
        raise NotImplementedError

    def start(self):
        # The entrance of a scheme
        self.set_parameter()
        iteration = 1
        if args.batch:
            iteration = int(raw_input("How many job sequences do you want to generate? Please enter an integer:"))
        for i in range(iteration):
            jobs = self.generate()
            self.record(jobs)

    # Write generated jobs to local storage
    def record(self, jobs):
        if (args.redir is None):
            directory = "job_base/" + self.__class__.__name__
            filename = self.__class__.__name__ + '_' + time.strftime("%y:%m:%d:%H:%M:%S.") + str(get_file_counter()) + ".txt"
        if (args.redir is not None):
            directory = "job_base/" + args.redir
            filename = str(get_file_counter()) + ".txt"
        if not os.path.exists(directory):
            os.makedirs(directory)
        serial = np.array([Job.serializeJob(job) for job in jobs])
        np.savetxt(directory + '/' + filename, serial)

class SchemeGeometricSets(JobsGenerationScheme):

    def get_helpinfo(self):
        return "In Scheme Geometric Sets, a set of conflicting jobs is generated in a way that each job is just covering the end point of its previous job, i.e. the conflicting interval should be of length 1. We let value of a job be equal to the length of the job in this scheme, and let length of a job grow as twice large as that of its previous job. Besides, a set of companion jobs will be generated in the same fashion but they are not conflicting with each other. Due to the exponential growth of job length, it is not allowed to have too many jobs. Thus, it is not uneffective to use --jl to specify the length of jobs, and there is no default for that."

    def __init__(self):
        self.name = "GeometricSets"

    def generate(self):
        print "Generate jobs using Scheme Geometric Sets" 
        
        # Geometric Set
        jobs = [Job(0, 1000, 1000, 0)] 
        for i in range(1, self.N):
            job = Job(jobs[i-1].arrival + jobs[i-1].duration - 1, jobs[i-1].duration * 2, jobs[i-1].value * 2, i)
            jobs.append(job)

        # Main Set
        for i in range(self.N - 1):
            job = Job(jobs[i].arrival + 1, jobs[i].duration - 1, jobs[i].value - 1, self.N + i)
            jobs.append(job)
        job_n = Job(jobs[self.N - 1].arrival + 1, jobs[self.N - 1].duration - 2, jobs[self.N - 1].value - 2, 2 * self.N - 1)
        jobs.append(job_n)
        job_n1 = Job(jobs[self.N - 1].arrival + jobs[self.N - 1].duration - 1, jobs[self.N - 1].duration * 2 - 1, jobs[self.N - 1].duration * 2 - 1, 2 * self.N)
        jobs.append(job_n1)
        return jobs

    def set_parameter(self):
        self.N = int(raw_input("Value of JOBS_AMOUNT would not be used for generating Geometric Sets, please enter the stage (size of geometric set) which will be a number between 10 and 30: "))
        if (self.N < 10 or self.N > 30):
            return self.set_parameter()
    
class SchemePUS(JobsGenerationScheme):

    # let f be input variable user can control and make y = x^2 a default choice
    def f(self, x):
        return x * x

    def get_helpinfo(self):
        return "In PUS scheme, the arriving time is determined by Poisson process; the length of a job follows a uniform distribution; f(x) = x^2 is the benevoent function. A parameter p is needed for the Poisson process and a range [a, b) is needed for the uniform distribution"

    def __init__(self):
        self.name = "PUS"

    def set_parameter(self):
        self.p = float(raw_input("Please enter p as a positive real number between 0 and 1:"))
        self.a = int(raw_input("Please enter range as a pair of integers (a,b), first enter a:"))
        self.b = int(raw_input("Then enter b:"))
        print "Please input benevonent function in the format \"lambda y: <function expression with respect to y>\", by default the function is set to f(y) = y * y"
        function_input = raw_input("Function:") 
        if (function_input is not None and len(function_input) != 0):
            self.f = eval(function_input)
        if (self.p <= 0 or self.p > 1 or self.a < 0 or self.b <= 0 or self.a > self.b):
            print "Invalid parameter, please enter them again"
            self.set_parameter()

    def generate(self):
        print "Generating jobs using PUS scheme"
        
        arrivals = []
        time = 0
        while len(arrivals) < JOBS_AMOUNT:
            if (np.random.randint(2)):
                arrivals.append(time)
            time += 1
        self.n = len(arrivals)
        durations = np.random.randint(low = self.a, high = self.b, size = self.n)
        values = self.f(durations) 
        
        jobs = [Job(arrivals[i], durations[i], values[i], i) for i in range(self.n)]

        return jobs

#SCHEMES is a list of currently available schemes objects
SCHEMES = []
JOBS_AMOUNT = args.jl 

def select_scheme():
    print "Which generating scheme do you want to use to generate jobs?"
    for i in range(len(SCHEMES)):
        print i + 1, ": ", SCHEMES[i].get_helpinfo()
    scheme_index = -1
    while scheme_index not in range(len(SCHEMES)):
        scheme_index = int(raw_input("Please select one available scheme: ")) - 1
    print "You chose the scheme ", SCHEMES[scheme_index].name
    return SCHEMES[scheme_index]

def init_generator():
    PUS = SchemePUS()
    SGS = SchemeGeometricSets()
    SCHEMES.append(PUS)
    SCHEMES.append(SGS)

def main():
    init_generator()
    is_exit = False
    while (not is_exit):
        scheme = select_scheme();
        scheme.start();
        exit_signal = raw_input("Do you want to exit? Y/N \n")
        while (exit_signal != "Y" and exit_signal != "N"):
            exit_signal = raw_input("Do you want to exit? Y/N \n")
        is_exit = "Y" == exit_signal
        
if __name__ == "__main__":
    main()
