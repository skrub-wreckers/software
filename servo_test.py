import tamproxy, tamproxy.devices
import pins
import time
import hal

if __name__ == '__main__':
	with tamproxy.TAMProxy() as tamp:
		print("init")
		servo = hal.Arm(tamp, 10)
		print("inited")

		while True:
			servo.down()
			raw_input()
			servo.up()
			time.sleep(0.75)
		