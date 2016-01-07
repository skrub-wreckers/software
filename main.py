import hal, tamproxy

if __name__ == '__main__':
	robot = hal.Robot(tamproxy.TAMProxy())
	robot.drive.turnIP(0.05)