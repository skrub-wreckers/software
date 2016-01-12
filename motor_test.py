import tamproxy, tamproxy.devices
import pins
import time

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        print("init")
        encoder = tamproxy.devices.Encoder(tamp, pins.l_encoder_a, pins.l_encoder_b)
        motor = tamproxy.devices.Motor(tamp, pins.l_motor_dir, pins.l_motor_pwm)
        print("inited")

        motor.write(1, 500)

        for i in range(10):
            print encoder.val
            time.sleep(0.05)
