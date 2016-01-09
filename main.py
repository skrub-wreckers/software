import hal, tamproxy

if __name__ == '__main__':
	robot = hal.Robot(tamproxy.TAMProxy())
	robot.drive.setDistSetpoint(6400)
	while(True):
		robot.drive.distPID()