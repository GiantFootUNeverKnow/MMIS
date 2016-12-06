#!/usr/bin/python
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Uncomment this line in Canopy
#plt.figure() 

for i in range(1,4):
    expectations = [0] * 19
    variances = [0] * 19
    directory = os.getcwd() + '/result' + str(i)
    for filename in os.listdir(directory):
        number = int(filename[8:])
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
    print "Avg: ", np.mean(expectations)
    print variances
    
    # Uncomment this line in Canopy
    #plt.plot(expectations, label = 'algorithm' + str(i))

# Uncomment this line in Canopy
#plt.legend()
#plt.show()
