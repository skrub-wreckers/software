from hal import *
from vision.window import Window
from vision import Camera
import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
	with TAMProxy() as tamproxy:
		drive = Drive(tamproxy)
		#arm = Arm(tamproxy, 10)
		#arm2 = Arm(tamproxy, 9)
		arms = Arms(tamproxy)

		w = Window("Eric")

		while True:

			c = chr(cv2.waitKey(1) & 0xFF)
			move_cmd = None


			if c == 'q':
				break
			elif c == 'w':
				move_cmd = (0.2, 0)

			elif c == 's':
				move_cmd = (-0.2, 0)

			elif c == 'a':
				move_cmd = (0, 0.2)

			elif c == 'd':
				move_cmd = (0, -0.2)

			elif c == ' ':
				arms.green.up()
				time.sleep(0.75)
				arms.green.down()

			elif c == 'c':
				arms.red.up()
				time.sleep(0.75)
				arms.red.down()

			if move_cmd:
				drive.l_enc.update()
				drive.r_enc.update()
				drive.go(*move_cmd)
				time.sleep(0.25)
				drive.stop()
				print drive.l_enc.val, drive.r_enc.val