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
			
			c = cv2.waitKey(1) & 0xFF
			if c == ord('q'):
				break
			elif c == ord('w'):
				drive.go(0.2)
				time.sleep(0.25)
				drive.go(0.0)
				
			elif c == ord('s'):
				drive.go(-0.2)
				time.sleep(0.25)
				drive.go(0.0)
				
			elif c == ord('a'):
				drive.turnIP(0.2)
				time.sleep(0.25)
				drive.turnIP(0.0)
				
			elif c == ord('d'):
				drive.turnIP(-0.2)
				time.sleep(0.25)
				drive.turnIP(0.0)
				
			elif c == ord(' '):
				arms.green.up()
				time.sleep(0.75)
				arms.green.down()
				
			elif c == ord('c'):
				arms.red.up()
				time.sleep(0.75)
				arms.red.down()