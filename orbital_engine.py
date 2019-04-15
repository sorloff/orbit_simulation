import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from position_calculator import calc_position, calc_accel



#holds fig, generates objects, runs animation
class Orbital_Engine:
	def __init__(self, count):
		#fix random state
		np.random.seed(1234567)
		self.pos_scale     = 1e6 #todo: utilitze these
		self.size_scale    = 1e6
		self.generate(count)
		self.animation = None
		self.margins   = [0, 10000, 0, 10000]


	#creates a list of stellar objects

	'''
	Stellar objects have the following structure:

	{
		star:   boolean        #is this object a star? used for aesthetic purposes only
		moon:   boolean        #is this object a moon? used for aesthetic purposes only
		loc:    [float, float] #location: x, y coords
		vel:    [float, float] #velocity: vx, vy
		accel:  [float, float] #acceleration: ax, ay
		radius: [float]                 
		mass:	[float]
	}
	'''
	#current test values are approx values of moon around earth
	def generate(self, count):
		#create objects
		self.objs = np.zeros(
			count,
			dtype = [
				("star", np.bool_, 1),
				("moon", np.bool_, 1),
				("loc", float, 2),
				("vel", float, 2),
				("accel", float, 2),
				("radius", float, 1),
				("mass", float, 1),
				("color", float, 3)
			]
		)

		#initialize objects
		self.objs["star"]   = False
		self.objs["moon"]   = False
		
		#elf.objs["loc"]    = np.random.uniform(500, 100000, (count, 2))
		self.objs["loc"] = np.asarray([[5e8, 5e8], [6.925e8, 3.075e8]])
		
		#self.objs["vel"]    = np.random.uniform(-1e2, 1e3, (count, 2))
		self.objs["vel"] = np.asarray([[0, 0], [2022e8, 2022e8]])

		#self.objs["radius"] = np.random.uniform(100, 1000, count)
		self.objs["radius"] = np.asarray([[6.371008e6, 1.7374e6]])
		
		#self.objs["mass"]   = np.random.uniform(1e7, 1e9, count)
		self.objs["mass"] = np.asarray([5.9721986e24, 7.3459e22])
		
		self.objs["color"]  = np.array([[1.0, 0.0, 1.0] for _ in range(len(self.objs))])

		#self.objs["accel"] = np.zeros((count, 2))
		self.objs["accel"]  = calc_accel(self.objs["loc"], self.objs["mass"])
		#self.objs["accel"][:, 0] = self.objs["accel"][:, 1]

		#return objects

	#scale the data down/up so it can be viewed easily
	def set_scale(self, data):
		pass

	def run_animation(self):
		#TODO: move facecolor settings to axes so it renders on video creation
		fig = plt.figure(figsize = (5, 5), facecolor="black")
		ax = fig.add_axes([0, 0, 1, 1], frameon=False, facecolor="black", autoscale_on=False)
		ax.set_xlim(0, 1e9), ax.set_xticks([])
		ax.set_ylim(0, 1e9), ax.set_yticks([])



		print("starting up...")

		print(self.objs)


		def update(frame):
			calc_position(self.objs)
			for row in self.objs: #TODO: this can probably run faster
				patches = plt.gca().patches
				if (len(patches) >= 2):
					patches[-1].remove()
				obj = plt.Circle(row["loc"], row["radius"], color="white")
				plt.gca().add_patch(obj)
			print(self.objs)


		print("about to run...")
		self.animation = FuncAnimation(fig, update, frames=1000, interval=0.1)
		#self.animation.save('orbit_test.mp4', dpi="figure", bitrate=5000)
		plt.show()
		print("that's all folks")