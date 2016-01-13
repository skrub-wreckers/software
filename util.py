import time

def clamp(value, min, max):
	if value < min: 
		return min
	elif value > max:
		return max
	else:
		return value


class Timer(object):
	def __init__(self, name, indent=''):
		self.name = name
		self.indent = indent
		self.has_children = False

	def __enter__(self):
		self.t = time.time()
		print(self.indent +'Timing {}... '.format(self.name), end='')
		return self

	def __exit__(self, *args):
		if self.has_children:
			print()
			print(self.indent + '  ' + str(time.time() - self.t))
		else:
			print(str(time.time() - self.t))

	def __call__(self, name):
		print()
		self.has_children = True
		return Timer(name, self.indent + '  ')

