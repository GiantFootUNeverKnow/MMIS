#!/usr/bin/python
import os
import matplotlib
import matplotlib.pyplot as plt

T = 150
directory = os.getcwd() + "/E26."
for i in range(1, 13):
    for j in range(1, 10001):
        a = open(directory + str(i) + '/' + "jobs/" + str(j) + '.txt', 'r+')
        lines = a.readlines()
        a.seek(0)
        if lines:
            trash = 0
            while (trash < len(lines) and float(lines[trash].split(None, 1)[0]) < T):
                a.write(lines[trash])
                trash += 1
        a.truncate()
        a.close()

