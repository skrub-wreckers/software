from hal import *
import vision
from vision.window import Window
from vision import Camera, Vision
import cv2
import math
import numpy as np

import constants

from tamproxy import TAMProxy

if __name__ == "__main__":
	with TAMProxy() as tamproxy:
		drive = Drive(tamproxy)
		#arm = Arm(tamproxy, 10)
		#arm2 = Arm(tamproxy, 9)
		arms = Arms(tamproxy)

		w = Window("Vision test")
		cam = Camera(geom=constants.camera_geometry)
		v = vision.Vision(cam)
		while True:

			v.update()
			angle = v.angle_to
			print angle, v.block_pos

			c = chr(cv2.waitKey(1) & 0xFF)
			if c == 'q':
				break
			elif c == ' ':
				if angle is None:
					arms.green.up()
					time.sleep(0.75)
					arms.green.down()
				elif abs(angle) < np.radians(5):

					dist = np.linalg.norm(v.block_pos)
					drive.go(0.25)
					time.sleep(dist / 10)
					drive.stop()
				else:
					rtime = abs(angle)/(math.pi*2)*4.45

					drive.turnIP(math.copysign(0.2, angle))
					time.sleep(rtime)
					drive.stop()