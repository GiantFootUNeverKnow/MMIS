#!/usr/bin/python
from scheduler import Scheduler, Machine
import unittest
import numpy as np

class SchedulerTester1(unittest.TestCase):
    '''
    Tester1 runs against toy dataset t1.txt, and Tester_k would run
 against dataset t_k.
    ''' 
    def setUp(self):
        self.scheduler = Scheduler()        
        jobs = np.loadtxt("TestCase/t1.txt")
        self.scheduler.jobs = np.array(sorted(jobs, key = lambda x:x[0]))

    def test_vanila_2(self):
        self.scheduler.mechanism = 0
        machine0 = Machine(1, 0)
        machine1 = Machine(1, 1)
        self.scheduler.machines = [machine0, machine1]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 86.0)
        self.assertEqual(machine1.total_value, 42.0)

    def test_vanila_3(self):
        self.scheduler.mechanism = 0
        machine0 = Machine(1, 0)
        machine1 = Machine(1, 1)
        machine2 = Machine(1, 2)
        self.scheduler.machines = [machine0, machine1, machine2]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 86.0)
        self.assertEqual(machine1.total_value, 42.0)
        self.assertEqual(machine2.total_value, 50.0)

    def test_priority_2(self):
        self.scheduler.mechanism = 1
        machine0 = Machine(2, 0)
        machine1 = Machine(2, 1)
        self.scheduler.machines = [machine0, machine1]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 98.0)
        self.assertEqual(machine1.total_value, 42.0)

    def test_priority_3(self):
        self.scheduler.mechanism = 1
        machine0 = Machine(1, 0)
        machine1 = Machine(2, 1)
        machine2 = Machine(3, 2)
        self.scheduler.machines = [machine0, machine1, machine2]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 86.0)
        self.assertEqual(machine1.total_value, 42.0)
        self.assertEqual(machine2.total_value, 50)

    def test_random_2(self):
        self.scheduler.mechanism = 2
        machine0 = Machine(2, 0)
        machine1 = Machine(2, 1)
        self.scheduler.machines = [machine0, machine1]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 98.0)
        self.assertEqual(machine1.total_value, 42.0)

    def test_low_wage_2(self):
        self.scheduler.mechanism = 3
        machine0 = Machine(2, 0)
        machine1 = Machine(2, 1)
        self.scheduler.machines = [machine0, machine1]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 98.0)
        self.assertEqual(machine1.total_value, 42.0)

 

 


if __name__ == '__main__':
    unittest.main()
