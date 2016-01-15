"""
Hardware Access Layer
"""
import util
import tamproxy
from tamproxy.devices import Motor, Servo, Encoder
import numpy as np
import time

import pins
import constants

class HardwareDevice:
	"""a device needing a connection through the arduino"""
	def __init__(obj, tamp):
		pass


class Drive(HardwareDevice):
	def __init__(self, tamp):
		self.lMotor = Motor(tamp, pins.l_motor_dir, pins.l_motor_pwm)
		self.lMotor.write(1,0)
		self.rMotor = Motor(tamp, pins.r_motor_dir, pins.r_motor_pwm)
		self.rMotor.write(1,0)

		self.r_enc = Encoder(tamp, pins.r_encoder_a, pins.r_encoder_b, continuous=False)
		self.l_enc = Encoder(tamp, pins.l_encoder_a, pins.l_encoder_b, continuous=False)

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
	def __init__(self, tamp, servo_pin, lower, upper):
		self.servo = Servo(tamp, servo_pin, lower, upper)

	def up(self):
		for angle in range(0, 40, 4):
			self.servo.write(angle)
			time.sleep(0.1)

		self.servo.write(180)

	def down(self):
		self.servo.write(0)

class Arms:
	def __init__(self, conn):
		self.green = Arm(conn, 9, lower=620, upper=2350)
		self.red = Arm(conn, 10, lower=2320, upper=500)


class Robot:
	def __init__(self, tamp):
		self.tamp = tamp
		if not self.tamp.started: self.tamp.start()
		self.arms = Arms(self.tamp)
		self.drive = Drive(self.tamp)

		self.camera = Camera(*constants.cameraResolution)
