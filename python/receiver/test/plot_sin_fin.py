import numpy 
#from pandas import read_csv
from scipy.optimize import curve_fit
from matplotlib import pyplot
import math
 

max_time = 0
min_value = 0
max_value = 0 
# define the true objective function
def objective(x, a, b, c):
	return numpy.sin((x * (3.1416))/(max_time)  + a) * (max_value-min_value) * b + c
 

x_line = [
17,
33,
50,
66,
82
]

y_line = [
122162,
104288,
114257,
117184,
97392
]
# create a line plot for the mapping function
#pyplot.plot(x_line, y_line, '--', color='red')
pyplot.scatter(x_line, y_line, color='red')
max_time = max(x_line)

min_value = min(y_line)
max_value = max(y_line)


popt, _ = curve_fit(objective, x_line, y_line)
a, b, c = popt
print('y = %.5f * x + %.5f * x^2 + %.5f' % (a, b, c))
# plot input vs output
# calculate the output for the range

out_x_line = [0] * (len(x_line) + 1)
out_y_line = [0] * (len(x_line) + 1)
for i in range(len(x_line)):
    out_x_line[i] = x_line[i]
    #out_y_line[i] = numpy.sin((x_line[i] * (2*3.1416))/(311))*2614722
    #out_y_line[i] = numpy.sin(x_line[i]/(311/4))*2614722 #
    out_y_line[i] = objective(x_line[i], a, b, c) 

nextTime = out_x_line[i]
nextval = objective(nextTime+10, a, b, c)     

out_x_line[i+1] = nextTime + 10
out_y_line[i+1] = nextval 
#pyplot.scatter(out_x_line, out_y_line, color='blue')
pyplot.plot(out_x_line, out_y_line, '--', color='blue')

pyplot.show()