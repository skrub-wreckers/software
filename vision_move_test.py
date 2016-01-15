from hal import *
from vision.window import Window
from vision import Camera, Vision
import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
	with TAMProxy() as tamproxy:
		drive = Drive(tamproxy)
		#arm = Arm(tamproxy, 10)
		#arm2 = Arm(tamproxy, 9)
		arms = Arms(tamproxy)

		w = Window("Vision test")
		v = vision.Vision()
		while True:

			c = chr(cv2.waitKey(1) & 0xFF)
			if c == 'q':
				break
			elif c == ' ':
				angle = v.update()
				print angle
				rtime = angle/360.0*1.13
				drive.turnIP(angle/abs(angle)*0.2)
				time.sleep(rtime)
				drive.turnIP(0.0)