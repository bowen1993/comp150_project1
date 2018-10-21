import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from ss import pstdev

def drawPlot(lines, filename, errBar=True):
    '''draw plots with given lines'''
    fig = plt.figure(num=None, figsize=(16, 9))
    ax1 = fig.add_subplot(111)
    for name in lines:
        line = lines[name]
        xs = np.array(line['x'])
        ys = np.array(line['y'])
        errBars = np.array(line['errorBar'])
        if errBar:
            ax1.errorbar(xs, ys, label=name, color=line['color'], yerr=errBars, fmt='o')
        else:
            ax1.plot(xs, ys, 'o')
        coeffs = np.polyfit(xs,ys,3)
        x2 = np.arange(min(xs)-0.1, max(xs)+0.1, .01)
        y2 = np.polyval(coeffs, x2)
        ax1.plot(x2,y2,color=line['color'], label="%s_regression" % name)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)
    plt.savefig('%s.png' % filename)
