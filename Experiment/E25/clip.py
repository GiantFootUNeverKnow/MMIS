#!/usr/bin/python
import os
import matplotlib
import matplotlib.pyplot as plt

ratios_reward = [0] * 24
expectations = [0] * 24
variances = [0] * 24
directory = os.getcwd() + "/E25."
j = 2
for i in range(1, 25):
    a = open(directory + str(i) + '/' + "result" + str(j))
    lines = a.readlines()
    if lines:
        firstline = lines[-3]
        secondline = lines[-2]
        thirdline = lines[-1]
        ratio_reward = float(firstline.rsplit(None, 1)[-1])
        expectation = float(secondline.rsplit(None, 1)[-1])
        variance = float(thirdline.rsplit(None, 1)[-1])
        ratios_reward[i - 1] = ratio_reward
        expectations[i - 1] = expectation
        variances[i - 1] = variance
    a.close()

print "ratios_reward: ", ratios_reward
print "expectations: ", expectations
print "variances: ", variances
