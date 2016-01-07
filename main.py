import hal, tamproxy

if __name__ == '__main__':
	robot = hal.Robot(tamproxy.TAMProxy())
	robot.drive.go(1, -1)