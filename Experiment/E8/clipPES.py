#!/usr/bin/python
import os
import matplotlib
import matplotlib.pyplot as plt

expectations = [0] * 19
variances = [0] * 19
directory = os.getcwd() + '/resultPES'
for filename in os.listdir(directory):
    number = int(filename[6:])
    a = open(directory + '/' + filename, 'rb')
    lines = a.readlines()
    if lines:
        firstline = lines[-2]
        secondline = lines[-1]
        expectation = float(firstline.rsplit(None, 1)[-1])
        variance = float(secondline.rsplit(None, 1)[-1])
        expectations[number - 1] = expectation
        variances[number - 1] = variance
    a.close()

print expectations
print variances
plt.figure()
plt.plot(expectations)
plt.figure()
plt.plot(variances)
plt.show()
