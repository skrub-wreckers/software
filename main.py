import hal, tamproxy
import time

if __name__ == '__main__':
	with tamproxy.TAMProxy() as proxy:
		robot = hal.Robot(proxy)
		robot.drive.setDistSetpoint(3200)
		currentTime = time.time()
		while(True):    
			if time.time() - currentTime > 0.001:
				currentTime = time.time()
				robot.drive.distPIDIterate()