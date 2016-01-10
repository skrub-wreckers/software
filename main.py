import hal, tamproxy

if __name__ == '__main__':
	robot = hal.Robot(tamproxy.TAMProxy())
	robot.drive.setSpeedSetpoint(500)
	while(True):
		robot.drive.speedPIDIterate()