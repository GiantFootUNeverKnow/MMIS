#!/usr/bin/python
import os
import matplotlib
import matplotlib.pyplot as plt

expectations = [0] * 9
variances = [0] * 9
directory = os.getcwd() + "/E16."
j = 12
for i in range(1, 10):
    a = open(directory + str(i + 9) + '/' + "result" + str(j))
    lines = a.readlines()
    if lines:
        firstline = lines[-2]
        secondline = lines[-1]
        expectation = float(firstline.rsplit(None, 1)[-1])
        variance = float(secondline.rsplit(None, 1)[-1])
        expectations[i - 1] = expectation
        variances[i - 1] = variance
    a.close()

print expectations
print variances
