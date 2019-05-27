import numpy as np
import math

#the gravitational constant
G = 6.673e-11
t = 5e-6#0.00001 #delta t

#calculates the next location of the objects for each frame
#equation used is verlet velocity scheme
def calc_position(objs):	
	objs["loc"]   = objs["loc"] + objs["vel"] * t + 0.5 * objs["accel"] * t**2
	objs["loc"]   = objs["loc"].clip(0, 1e9)
	a_t           = objs["accel"]
	objs["accel"] = calc_accel(objs["loc"], objs["mass"])
	objs["vel"]   = objs["vel"] + 0.5 * (a_t + objs["accel"]) * t

	return objs

#calcs acceleration in the x and y directions
#this is a test func for the 2-body problem
def calc_accel(objs_loc, objs_m):
	x_1 = objs_loc[0, 0]
	y_1 = objs_loc[0, 1]
	x_2 = objs_loc[1, 0]
	y_2 = objs_loc[1, 1]

	m_1 = objs_m[0]
	m_2 = objs_m[1]

	#delta x
	d_x = x_1 - x_2

	#delta y
	d_y = y_1 - y_2

	#|r|^3
	r_3 = math.sqrt(d_x**2 + d_y**2)

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

	return np.asarray([ 
		[x1_a, y1_a],
		[x2_a, y2_a]
	])