""" pin configuration on the teensy """

# by convention, when there is both a left and a right pin, the left pin should
# be closer to the usb port

# analog pins, for readability
A = range(21)


l_ir_long = A[3]
r_ir_long = A[2]
l_ir_short = 15
r_ir_short = 14
back_ir_short = 33

l_bumper = 0
r_bumper = 3

# breakbeams
l_bb_send = 32
r_bb_send = 31

r_motor_pwm = 23
r_motor_dir = 22
l_motor_pwm = 21
l_motor_dir = 20

r_encoder_a = 28
r_encoder_b = 27
l_encoder_a = 30
l_encoder_b = 29

l_arm = 9
r_arm = 10

stack_door = 4
stack_latch = 5

gyro_cs = 24

photo_resistor = 0 #placeholder
led = 0 #placeholder
