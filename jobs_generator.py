#!/usr/bin/python

import numpy as np
import os
import time

"""
A general class for job generation scheme. Any variation of the scheme can be added as subclass of this class
start() is the entrance of any operations of a scheme
"""
class JobsGenerationScheme(object):

    # Abstract function that must be implemted in the subclass
    def get_helpinfo(self):
        # return description of the scheme
        raise NotImplementedError

    # Abstract function that must be implemted in the subclass
    def __init__(self):
        raise NotImplementedError

    # Abstract function that must be implemted in the subclass
    def generate(self):
        # Generate job sequence and return
        raise NotImplementedError

    # Abstract function that must be implemted in the subclass
    def start(self):
        # The entrance of a scheme
        raise NotImplementedError

    # Write generated jobs to local storage
    def record(self, jobs):
        directory = "job_base/" + self.__class__.__name__
        filename = self.__class__.__name__ + '_' + time.strftime("%y:%m:%d:%H:%M:%S") + ".txt"
        if not os.path.exists(directory):
            os.makedirs(directory)
        np.savetxt(directory + '/' + filename, jobs, '''fmt="%d"''')

class SchemePUS(JobsGenerationScheme):

    def f(self, x):
        return x * x

    def get_helpinfo(self):
        return "In PUS scheme, the arriving time is determined by Poisson distribution; the length of a job follows a uniform distribution; f(x) = x^2 is the benevoent function. A parameter lambda is needed for the Poisson distribution and a range [a, b) is needed for the uniform distribution"

    def __init__(self):
        self.name = "PUS"
        self.n = JOBS_AMOUNT

    def set_parameter(self):
        self.lamb = float(raw_input("Please enter lambda as a positive real number:"))
        self.a = int(raw_input("Please enter range as a pair of integers (a,b), first enter a:"))
        self.b = int(raw_input("Then enter b:"))
        if (self.lamb <= 0 or self.a < 0 or self.b <= 0 or self.a > self.b):
            print "Invalid parameter, please enter them again"
            self.set_parameter()

    def generate(self):
        print "Generating jobs using PUS scheme"
        jobs = np.zeros((self.n, 3), dtype = np.int)
        # Randomly generate arrival time of jobs by a poisson random variable
        jobs[:, 0] = np.random.poisson(self.lamb, self.n)
        # Randomly generate duration of jobs by a discrete uniform distribution
        jobs[:, 1] = np.random.randint(low = self.a, high = self.b, size = self.n)
        # Calculate values of the jobs by function f(x)
        jobs[:, 2] = self.f(jobs[:, 1])
        print jobs
        return jobs

    def start(self):
        self.set_parameter()
        jobs = self.generate()
        self.record(jobs)

#SCHEMES is a list of currently available schemes objects
SCHEMES = []
JOBS_AMOUNT = 999

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
    SCHEMES.append(PUS)

def main():
    init_generator()
    is_exit = False
    while (not is_exit):
        scheme = select_scheme();
        scheme.start();
        is_exit = "Y" == raw_input("Do you want to exit? Y/N \n")

if __name__ == "__main__":
    main()
