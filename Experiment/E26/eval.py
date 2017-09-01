#!/usr/bin/python
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

T = 150
opts = [0] * 12
ls = [0] * 12
vs = [0] * 12
directory = os.getcwd() + "/E26."
for i in range(1, 13):
    a = open(directory + str(i) + '/' + "result")
    lines = a.readlines()
    if lines:
        firstline = lines[1]
        opt = float(firstline.rsplit(None, 1)[-1])
        opts[i - 1] = opt
    a.close()

for i in range(1, 13):
    l = []
    v = []
    for j in range(1, 10001):
        f = open(directory + str(i) + '/jobs/' + str(j) + '.txt')
        lines = f.readlines()
        if lines:
            for k in range(len(lines)):
                v.append(float(lines[k].split()[2]))
                l.append(float(lines[k].split()[1]))
    ls[i - 1] = np.average(l)
    vs[i - 1] = np.average(v)

print "E[OPT]: ", opts
print "E[L]: ", ls
print "E[V]: ", vs
print "T / E[l] * E[v]: ", [T * 1.0 / ls[i] * vs[i] for i in range(12)]
