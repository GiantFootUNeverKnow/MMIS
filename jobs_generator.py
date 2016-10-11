#!/usr/bin/python

import numpy as np
import os
import argparse
import time

parser = argparse.ArgumentParser();
parser.add_argument('--batch', action='store_const', const=True, default=False, help='Switch to batch mode. By default, all generated jobs will still be stored in the directory named after the generation scheme as usual, but we recommend you to use --redir to redirect batch jobs to a separate directory ')
parser.add_argument('--redir', help='Specify name of a directory to store the generated jobs')
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
        directory = "job_base/" + self.__class__.__name__
        # TODO add index to the timestamp to prevent rewriting
        filename = self.__class__.__name__ + '_' + time.strftime("%y:%m:%d:%H:%M:%S") + ".txt"
        if (args.redir is not None):
            directory = "job_base/" + args.redir
            filename = str(get_file_counter()) + ".txt"
        if not os.path.exists(directory):
            os.makedirs(directory)
        np.savetxt(directory + '/' + filename, jobs)

class SchemePUS(JobsGenerationScheme):

    # TODO let f be input variable user can control and make y = x^2 a default choice
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
        if (self.p <= 0 or self.p > 1 or self.a < 0 or self.b <= 0 or self.a > self.b):
            print "Invalid parameter, please enter them again"
            self.set_parameter()

    def generate(self):
        print "Generating jobs using PUS scheme"
        odds = np.random.randint(2, size = DEFAULT_JOBS_AMOUNT)        
        
        arrivals = [i for i in range(DEFAULT_JOBS_AMOUNT) if odds[i] == 1]
        self.n = len(arrivals)
        durations = np.random.randint(low = self.a, high = self.b, size = self.n)
        values = self.f(durations) 
        
        # TODO Use Job Constructor
        jobs = np.array([arrivals, durations, values, np.array(range(self.n))], dtype = np.int).T
        
        print jobs
        return jobs

#SCHEMES is a list of currently available schemes objects
SCHEMES = []
# TODO make this variable controlled by user
DEFAULT_JOBS_AMOUNT = 999

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
        exit_signal = raw_input("Do you want to exit? Y/N \n")
        while (exit_signal != "Y" and exit_signal != "N"):
            exit_signal = raw_input("Do you want to exit? Y/N \n")
        is_exit = "Y" == exit_signal
        
if __name__ == "__main__":
    main()
