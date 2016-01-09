from constants import *
		
def clamp(value, min, max):
	if value < min: 
		return min
	elif value > max:
		return max
	else:
		return value

class PID:
	def __init__(self, kP, kI, kD, setpoint=0):
		self.kP = kP
		self.kI = kI
		self.kD = kD
		self.setSetpoint(setpoint)

	def setSetpoint(self, setpoint):
		self.setpoint = setpoint
		self.prevErr = 0
		self.integral = 0

	def iterate(self, val):
		err = self.setpoint - val
		self.integral += err
		derivative = (err - prevErr)
		self.prevErr = err
		return self.kP * err + self.kI * integral + self.kD * derivative


