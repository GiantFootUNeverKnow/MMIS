import numpy as np

class Job(object):
    def __init__(self, arrival, duration, value, name):
        self.arrival = arrival
        self.duration = duration
        self.value = value
        self.name = name
        self.set_yfactor()
    
    def set_yfactor(self):
        self.yfactor = np.random.random()

    def floor(self):
        self.arrival = np.floor(self.arrival)
        self.duration = np.floor(self.duration)
        self.value = np.floor(self.value)
        self.name = np.floor(self.name)

    @staticmethod
    def deserializeJob(data):
        return Job(data[0], data[1], data[2], data[3])

    @staticmethod
    def serializeJob(job):
        return np.array([job.arrival, job.duration, job.value, job.name])
