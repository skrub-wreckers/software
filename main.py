import hal, tamproxy
import time

if __name__ == '__main__':
	# with tamproxy.TAMProxy() as proxy:
		robot = hal.Robot(tamproxy.TAMProxy())
		robot.drive.go(1,0)
		# robot.drive.setSpeedSetpoint(100)
		dumb = True
		currentTime = time.time()
		while(True):    
			if time.time() - currentTime > 1:
				currentTime = time.time()
				if dumb:
					print "Off"
					robot.drive.stop()
				else:
					print "On"
					robot.drive.go(1,0)
				dumb = not dumb
			# robot.drive.speedPIDIterate() 