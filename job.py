import numpy as np

class Job(object):
    def __init__(self, arrival, duration, value, name):
        self.arrival = arrival
        self.duration = duration
        self.value = value
        self.name = name

    @staticmethod
    def deserializeJob(data):
        return Job(data[0], data[1], data[2], data[3])

    @staticmethod
    def serializeJob(job):
        return np.array([job.arrival, job.duration, job.value, job.name])
