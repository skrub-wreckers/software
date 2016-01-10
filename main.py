import hal, tamproxy

if __name__ == '__main__':
	robot = hal.Robot(tamproxy.TAMProxy())
	# robot.drive.setSpeedSetpoint(100)
	robot.drive.go(0.2, 0)
	while(True):
		robot.drive.speedPIDIterate()

		# Add logging and check it out