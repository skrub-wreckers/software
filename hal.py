"""
Hardware Access Layer
"""
import util
import tamproxy
from tamproxy.devices import Motor
from tamproxy.devices import Encoder
import constants
import pins

class HardwareDevice:
	"""a device needing a connection through the arduino"""
	def __init__(obj, tamp):
		pass

class Drive(HardwareDevice):
	def __init__(self, tamp):
		self.lMotor = tamproxy.devices.Motor(tamp, pins.l_motor_dir, pins.l_motor_pwm)
		self.rMotor = tamproxy.devices.Motor(tamp, pins.r_motor_dir, pins.r_motor_pwm)
		self.currentThrottle = 0
		self.currentSteer = 0
		self.stop()

		self.lEncoder = tamproxy.devices.Encoder(tamp, pins.l_encoder_a, pins.l_encoder_b)
		self.prevEncoderVal = 0

		self.speedPID = util.PID(kP=constants.motor_speed_p, kI=constants.motor_speed_i, kD=constants.motor_speed_d)
		self.anglePID = util.PID(kP=constants.motor_angle_p, kI=constants.motor_angle_i, kD=constants.motor_angle_d)

	def go(self, throttle, steer=0):
		"""both arguments measured in [-1 1], steer=-1 is CW"""
		lPow = rPow = throttle
		lPow -= steer
		rPow += steer
		self.lMotor.write(lPow>0, util.clamp(abs(255 * lPow), 0, 255))
		self.rMotor.write(rPow>0, util.clamp(abs(255 * rPow), 0, 255))
		self.currentThrottle = throttle
		self.currentSteer = steer
		
	def turnIP(self, throttle):
		"""turn in place arg is in [-1 1] with -1 full speed CW"""
		self.lMotor.write(-throttle>0, util.clamp(abs(255 * throttle), 0, 255))
		self.rMotor.write(throttle>0, util.clamp(abs(255 * throttle), 0, 255))
	
	def stop(self):
		self.go(throttle=0)

	def setSpeedSetpoint(self, val):
		self.speedPID.setSetpoint(val)

	def speedPIDIterate(self):
		"""Adjusts the throttle value of the drive"""
		val = self.lEncoder.val
		print val
		# speed = val - self.prevEncoderVal
		# power = self.speedPID.iterate(speed) 	
		# self.prevEncoderVal = val

		# # Do we need something for each individual motor?
		# # Also does this even make sense?
		# self.go(util.clamp(self.currentThrottle + power, -1, 1), self.currentSteer) 

	def anglePIDIterate(self):
		"""Adjusts the steer value of the drive"""
		pass

class Arm(HardwareDevice):
	def up(self):
		pass

	def down(self):
		pass


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
