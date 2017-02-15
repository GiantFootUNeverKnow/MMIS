#!/usr/bin/python
import os
import matplotlib
import matplotlib.pyplot as plt

expectations = [0] * 19
variances = [0] * 19
directory = os.getcwd() + '/result'
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
x = [x * 0.05 for x in range(1, 20)]
plt.figure()
plt.plot(x, expectations, label = 'Expected Competitive Ratio')
plt.legend()
plt.figure()
plt.plot(x, variances, label = 'Variance of Competitive Ratio')
plt.legend()
plt.show()