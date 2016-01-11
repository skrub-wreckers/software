import hal, tamproxy
import time

if __name__ == '__main__':
	with tamproxy.TAMProxy() as proxy:
		robot = hal.Robot(proxy)
		# robot.drive.setSpeedSetpoint(100)
		dumb = True
		encoder = False
		currentTime = time.time()
		encoderTime = time.time()
		while(True):    
			if time.time() - currentTime > 1:
				currentTime = time.time()
				robot.drive.speedPIDIterate()
				if dumb:
					print "Off"
					robot.drive.stop()
				else:
					print "On"
					robot.drive.go(0.1,0)
				dumb = not dumb				
			# if time.time() - currentTime > 0.1:
			# 	currentTime = time.time()
			if not encoder and time.time() - encoderTime > 5:
				print "Encoder Started"
				encoder = True
				# robot.drive.startEncoder()