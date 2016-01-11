import hal, tamproxy
from tamproxy import Sketch, SyncedSketch, Timer

class MainRobot(SyncedSketch):
	def setup(self):
		self.robot = hal.Robot(self.tamp)
		self.robot.drive.setDistSetpoint(3200)
		self.timer = Timer()

	def loop(self):
		if self.timer.millis() > 10:
			self.timer.reset()
			self.robot.drive.distPIDIterate()

if __name__ == "__main__":
	sketch = MainRobot(1, -0.00001, 100) # Ratio, gain, interval
	sketch.run()
	