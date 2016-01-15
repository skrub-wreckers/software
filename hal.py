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
		"""both arguments measured in [-1 1], steer=-1 is full speed CW"""
		lPow = rPow = throttle
		lPow -= steer
		rPow += steer
		self.lMotor.write(lPow>0, util.clamp(abs(255 * lPow), 0, 255))
		self.rMotor.write(rPow>0, util.clamp(abs(255 * rPow), 0, 255))

	def turnIP(self, throttle):
		"""turn in place arg is in [-1 1] with -1 full speed CW"""
		self.go(0, steer=throttle)

	def stop(self):
		self.go(throttle=0)

class Arm(HardwareDevice):
	def __init__(self, tamp, servo_pin):
		self.servo = Servo(tamp, servo_pin)

	def up(self):
		for angle in range(620, 1020, 40):
			self.servo.write(angle)
			time.sleep(0.1)
		self.servo.write(2400)

	def down(self):
		self.servo.write(620)

class Arms:
	def __init__(self, conn):
		self.green = Arm(conn)
		self.red = Arm(conn)


class Robot:
	def __init__(self, tamp):
		self.tamp = tamp
		if not self.tamp.started: self.tamp.start()
		self.arms = Arms(self.tamp)
		self.drive = Drive(self.tamp)

		self.camera = Camera(*constants.cameraResolution)
