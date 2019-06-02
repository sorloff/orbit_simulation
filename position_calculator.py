import numpy as np
#import cupy as np
import math
from timeit import default_timer as timer

#TODO: general speed optimization

#the gravitational constant
G = 6.673e-11
#delta t
#TODO: speed up calc, up this factor and only display every x frames to decrease error
#t = 5e-6 
t = 100

#calculates the next location of the objects for each frame
#equation used is verlet velocity scheme
def calc_position(objs):	
	objs["loc"]   = objs["loc"] + objs["vel"] * t + 0.5 * objs["accel"] * t**2
	objs["loc"]   = objs["loc"].clip(0, 1e9)
	a_t           = objs["accel"]
	objs["accel"] = calc_accel_linear(objs["loc"], objs["mass"])
	#objs["accel"] = calc_accel(objs["loc"], objs["mass"])

	objs["vel"]   = objs["vel"] + 0.5 * (a_t + objs["accel"]) * t

	return objs

#gets delta between simple accel and linear accel functions
def get_delta(objs_loc, objs_m):
	return calc_accel(objs_loc, objs_m) - calc_accel_linear(objs_loc, objs_m)

#calcs acceleration in the x and y directions
#this is a test func for the 2-body problem
def calc_accel(objs_loc, objs_m):
	#start = timer()

	x_1 = objs_loc[0, 0]
	y_1 = objs_loc[0, 1]
	x_2 = objs_loc[1, 0]
	y_2 = objs_loc[1, 1]

	m_1 = objs_m[0]
	m_2 = objs_m[1]

	#delta x
	d_x = x_1 - x_2


	#print(d_x)

	#delta y
	d_y = y_1 - y_2

	#print(d_y)

	#|r|^3
	r_3 = math.sqrt(d_x**2 + d_y**2)**3

	#print(r_3)

	if (r_3 == 0):
		return np.asarray([
				[0, 0],
				[0, 0]
			])

	#begin full calcs

	x1_a = (G * m_2 * d_x * -1) / r_3
	y1_a = (G * m_2 * d_y * -1) / r_3

	x2_a = (G * m_1 * d_x) / r_3
	y2_a = (G * m_1 * d_y) / r_3

	#end = timer()

	#print("simple elapsed time:", end - start)

	return np.asarray([ 
		[x1_a, y1_a],
		[x2_a, y2_a]
	])

#calcs acceleration in the x and y directions
#uses fancy linear algebra magic
#TODO: see if x/y parts can't be done at once
def calc_accel_linear(objs_loc, objs_m):
	#start = timer()

	#vector of x, y coords
	x_v = objs_loc[:,0]
	y_v = objs_loc[:,1]

	#number of objs
	n = x_v.size

	#stack those vectors
	#stacks downwards
	x_m = np.tile(x_v, (n, 1))
	y_m = np.tile(y_v, (n, 1))

	#subtract from the transpose to get the deltas
	d_x = x_m - x_m.T
	d_y = y_m - y_m.T

	#distance cubed
	r_3 = np.power(np.sqrt(np.power(d_x, 2) + np.power(d_y, 2)), 3)

	m_m = np.tile(objs_m, (n, 1))

	z_x = (m_m * d_x).T
	z_y = (m_m * d_y).T

	a_x = np.sum(np.nan_to_num((G * z_x) / r_3), 0)
	a_y = np.sum(np.nan_to_num((G * z_y) / r_3), 0)

	a = np.stack((a_x, a_y), axis=-1)

	#end = timer()

	#print("numpy elapsed time:", end - start)

	return a