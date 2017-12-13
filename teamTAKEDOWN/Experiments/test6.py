import numpy as np
import scipy.stats
#return the least-squares solution to a linear matrix equation.
import matplotlib.pyplot as plt

xi = np.arange(0,9)
A = np.array([ xi, np.ones(9)])
# linearly generated sequence
y = [19, 20, 20.5, 21.5, 22, 23, 23, 25.5, 24]

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(xi,y)
line = slope*xi+intercept
content='R:'+str(r_value)+' P:'+str(p_value)+' Standard Deviation:'+str(std_err)
title="Count:"+str(len(y))+' [Y]='+str(slope)+'[X]+'+str(intercept)
fig = plt.figure()
fig.canvas.set_window_title(content)
plt.title(title)
for index, xy in enumerate(zip(xi, y)):
    plt.annotate('(%s, %s)' % (int(xy[0]), int(xy[1])), xy=xy)
plt.plot(xi,line,'r-',xi,y,'o')
plt.show()
