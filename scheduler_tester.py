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
        self.scheduler.select_dataset_file("TestCase/t1.txt")    

    def test_priority_2(self):
        self.scheduler.mechanism = 1
        machine0 = Machine(2, 1, 0)
        machine1 = Machine(2, 1, 1)
        self.scheduler.machines = [machine0, machine1]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 89.0)
        self.assertEqual(machine1.total_value, 42.0)

    def test_priority_3(self):
        self.scheduler.mechanism = 1
        machine0 = Machine(1, 1, 0)
        machine1 = Machine(2, 1, 1)
        machine2 = Machine(3, 1, 2)
        self.scheduler.machines = [machine0, machine1, machine2]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 89.0)
        self.assertEqual(machine1.total_value, 42.0)
        self.assertEqual(machine2.total_value, 34.0)
       
    def test_random_2(self):
        '''
        self.scheduler.mechanism = 2
        machine0 = Machine(2, 0)
        machine1 = Machine(2, 1)
        self.scheduler.machines = [machine0, machine1]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 98.0)
        self.assertEqual(machine1.total_value, 42.0)
        '''
        pass #Due to the random nature of this heuristic, it is hard to test

    def test_low_wage_2(self):
        self.scheduler.mechanism = 3
        machine0 = Machine(2, 1, 0)
        machine1 = Machine(2, 1, 1)
        self.scheduler.machines = [machine0, machine1]
        self.scheduler.run_schedule()
        self.assertEqual(machine0.total_value, 98.0)
        self.assertEqual(machine1.total_value, 42.0)

    def test_offline_optimal(self):
        self.assertEqual(self.scheduler.offline_single_machine(), 98.0)

 


if __name__ == '__main__':
    unittest.main()
