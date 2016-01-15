import tamproxy, tamproxy.devices
import pins
import time

sval = 1500
step = 50

if __name__ == '__main__':
	with tamproxy.TAMProxy() as tamp:
		print("init")
		#servo = tamproxy.devices.Servo(tamp,10)
		pin = tamproxy.devices.DigitalOutput(tamp,10)
		print("inited")
		pin.write(True)
		raw_input()
		pin.write(False)

		#servo.write(sval)
		#while True:
		#	if raw_input() == "u":
		#		sval-=step
		#	else:
		#		sval+=step
		#	print sval
		#	servo.write(sval)
			