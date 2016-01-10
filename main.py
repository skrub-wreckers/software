import hal, tamproxy
import time

if __name__ == '__main__':
	with tamproxy.TAMProxy() as proxy:
		robot = hal.Robot(proxy)
		# robot.drive.setSpeedSetpoint(100)
		robot.drive.go(0.1, 0)
		while(True):
			robot.drive.speedPIDIterate()