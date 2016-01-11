import hal, tamproxy
from tamproxy import Sketch, SyncedSketch, Timer
import time

class MainRobot(SyncedSketch):
	def setup(self):
		self.robot = hal.Robot(self.tamp)
		self.robot.drive.setDistSetpoint(3200)
		self.timer = Timer()
		self.currentTime = time.time()
		self.flip = True

	def loop(self):
		if self.timer.millis() > 10:
			self.timer.reset()
			self.robot.drive.distPIDIterate()
		if time.time() - self.currentTime > 0.5:
			self.currentTime = time.time()
			if self.flip:
				self.robot.drive.go(0.2,0)
			else:
				self.robot.drive.stop()
			self.flip = not self.flip


if __name__ == "__main__":
	sketch = MainRobot(1, -0.00001, 100) # Ratio, gain, interval
	sketch.run()
	