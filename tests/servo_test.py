import tamproxy, tamproxy.devices
import time
from sw import pins

import cv2


if __name__ == '__main__':
	with tamproxy.TAMProxy() as tamp:
		# Make the trackbar used for HSV masking

		print("init")
		servo = tamproxy.devices.Servo(tamp,pins.l_arm)
		# pin = tamproxy.devices.DigitalOutput(tamp,10)
		# print("inited")
		# pin.write(True)
		# raw_input()
		# pin.write(False)

		cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
		cv2.createTrackbar('Position','frame', 1500,3000, servo.write_microseconds)

		while True:
			c = chr(cv2.waitKey(1) & 0xFF)
			if c in ('q', '\x1b'):
				break