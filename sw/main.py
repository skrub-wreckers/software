import hal, tamproxy
import time

if __name__ == '__main__':
	with tamproxy.TAMProxy() as proxy:
		robot = hal.Robot(proxy)
		robot.drive.go(steer=0.05)
		time.sleep(2)
