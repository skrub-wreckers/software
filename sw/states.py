class StateManager(object):
	"""
	Class for managing states of the robot
	"""
	def __init__(self, default):
		self.currentState = default
		self.states = []

	def run(self):
		self.currentState.execute()

class State(object):
	"""
	Base class for command.
	"""
	def __init__(self, robot):
		self.robot = robot
		pass

	# run continously while state is active
	def execute(self):
		if(self.isFinished()):
			end()
		pass

	# called periodically to see if state is over
	def isFinished(self):
		return False

	# called at the end of the state
	def end(self):
		pass

class SpinInPlace(State):
	"""
	State for spinning in place
	"""
	def __init__(self, robot):
		pass

	def execute(self):
		self.robot.drive.turnIP(0.05)

class WallFollowing(State):
	"""
	State for wall following
	"""
	def __init__(self, robot):
		pass