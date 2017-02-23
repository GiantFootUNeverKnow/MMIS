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
        self.assertEqual(machine1.total_value, 30.0)
        self.assertEqual(machine2.total_value, 25.0)
       
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

    def test_offline_optimal1(self):
        self.assertEqual(self.scheduler.offline_single_machine(), 98.0)

    def test_offline_optimal2(self):
        self.assertEqual(self.scheduler.offline_double_machine(), 149.0)

    def test_competitive_ratio(self):
        # TODO add this test
        pass 

class SchedulerTester2(unittest.TestCase):
    '''
    Tester2 runs against toy dataset t2.txt, and Tester_k would run
 against dataset t_k.
    ''' 
    def setUp(self):
        self.scheduler = Scheduler()        
        self.scheduler.select_dataset_file("TestCase/t2.txt")    

    def test_priority_1_5(self):
        self.scheduler.mechanism = 1
        machine0 = Machine(1.5, 1, 0)
        self.scheduler.machines = [machine0]
        self.scheduler.run_schedule()
        self.assertEqual(np.floor(machine0.total_value), 16834112.0)

    def test_priority_2(self):
        self.scheduler.mechanism = 1
        machine0 = Machine(2, 1, 0)
        self.scheduler.machines = [machine0]
        self.scheduler.run_schedule()
        self.assertEqual(np.floor(machine0.total_value), 75751478.0)


class SchedulerTester3(unittest.TestCase):
    '''
    Tester3 runs against toy dataset t3.txt, and Tester_k would run 
    against dataset t_k
    '''
    def setUp(self):
        self.scheduler = Scheduler()
        self.scheduler.select_dataset_file("TestCase/t3.txt")

    def test_offline_optimal1(self):
        self.assertEqual(self.scheduler.offline_single_machine(), 6.0)

    def test_offline_optimal2(self):
        self.assertEqual(self.scheduler.offline_double_machine(), 11.0)

class SchedulerTester4(unittest.TestCase):
    '''
    Tester4 runs against toy dataset t4.txt, and Tester_k would run 
    against dataset t_k
    '''
    def setUp(self):
        self.scheduler = Scheduler()
        self.scheduler.select_dataset_file("TestCase/t4.txt")

    def test_offline_optimal1(self):
        self.assertEqual(self.scheduler.offline_single_machine(), 6.0)

    def test_offline_optimal2(self):
        self.assertEqual(self.scheduler.offline_double_machine(), 10.0)

class SchedulerTester5(unittest.TestCase):
    '''
    Tester5 runs against toy dataset t5.txt, and Tester_k would run 
    against dataset t_k
    '''
    def setUp(self):
        self.scheduler = Scheduler()
        self.scheduler.select_dataset_file("TestCase/t5.txt")

    def test_offline_optimal1(self):
        self.assertEqual(self.scheduler.offline_single_machine(), 13.0)

    def test_offline_optimal2(self):
        self.assertEqual(self.scheduler.offline_double_machine(), 25.0)

if __name__ == '__main__':
    unittest.main()
