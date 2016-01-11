"""
Hardware Access Layer
"""
import util
import tamproxy
from tamproxy.devices import Motor
import cv2
import numpy as np

import pins
import constants

class HardwareDevice:
	"""a device needing a connection through the arduino"""
	def __init__(obj, tamp):
		pass


class Drive(HardwareDevice):
	def __init__(self, tamp):
		self.lMotor = tamproxy.devices.Motor(tamp, pins.l_motor_dir, pins.l_motor_pwm)
		self.lMotor.write(1,0)
		self.rMotor = tamproxy.devices.Motor(tamp, pins.r_motor_dir, pins.r_motor_pwm)
		self.rMotor.write(1,0)
		
	def go(self, throttle, steer=0):
		"""both arguments measured in [-1 1], steer=-1 is CW"""
		lPow = rPow = throttle
		lPow -= steer*0.1
		rPow += steer*0.1
		self.lMotor.write(lPow>0, util.clamp(abs(255 * lPow), 0, 255))
		self.rMotor.write(rPow>0, util.clamp(abs(255 * rPow), 0, 255))
		
	def turnIP(self, throttle):
		"""turn in place arg is in [-1 1] with -1 full speed CW"""
		self.lMotor.write(-throttle>0, util.clamp(abs(255 * throttle), 0, 255))
		self.rMotor.write(throttle>0, util.clamp(abs(255 * throttle), 0, 255))
	
	def stop(self):
		self.go(throttle=0)

class Arm(HardwareDevice):
	def up(self):
		pass

	def down(self):
		pass

class Arms:
	def __init__(self, conn):
		self.green = Arm(conn)
		self.red = Arm(conn)
		
class Camera:
	def __init__(self):
		self.cameraCon = cv2.VideoCapture(constants.cameraID)
		self.cameraCon.set(cv2.CAP_PROP_FRAME_WIDTH, constants.cameraResolution[0])
		self.cameraCon.set(cv2.CAP_PROP_FRAME_HEIGHT, constants.cameraResolution[1])
		if constants.cameraDebug:
			cv2.namedWindow("Raw")
			
	def getColorGroups(self):
		ret, frame = cap.read()
		if not ret:
			print('No frame')
			continue #Handle this better?
		
		colorGroups = {}
		for color in constants.planes:
			colorGroups[color] = np.ones(frame.shape)
			for plane in constants.planes[color]:
				colorGroups[color] = colorGroups[color] and util.threshold(plane, frame)
		
		return colorGroups
		
	def getBlobs(self, colorGroups):
		pass
		
class Robot:
	def __init__(self, tamp):
		self.tamp = tamp
		if not self.tamp.started: self.tamp.start()
		self.arms = Arms(self.tamp)
		self.drive = Drive(self.tamp)
