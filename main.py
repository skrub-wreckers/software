import hal, tamproxy
import time

if __name__ == '__main__':
	with tamproxy.TAMProxy() as proxy:
		robot = hal.Robot(proxy)
		# robot.drive.setDistSetpoint(3200)
		robot.drive.go(0.1, 0)
		currentTime = time.time()
		while(True):    
			if time.time() - currentTime > 0.01:
				currentTime = time.time()
				robot.drive.speedPIDIterate()
				# robot.drive.distPIDIterate()